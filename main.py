import logging
import asyncio
import keyboards
from keyboards import *
from read_content import *
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from config import TOKEN
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class FilmSearch(StatesGroup):
    waiting_for_keyword = State()
    sign = State()
    year = State()
    genre = State()
    s_prefix_sign = State()
    s_prefix_year = State()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"<strong>Привет! Я могу подобрать для вас интересный фильм, по вашим параметрам. Есть несколько вариантов поиска фильмов:</strong>", parse_mode='html', reply_markup=keyboards.b2)


@dp.callback_query(F.data == 'film_name')
async def film_name_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали поиск по ключевому слову')
    await callback.message.answer(f"<strong>Пожалуйста, введите ключевое слово для поиска. Вы увидите все фильмы, в названии которых присутствует это слово.</strong>", parse_mode='html')
    await state.set_state(FilmSearch.waiting_for_keyword)
@dp.message(FilmSearch.waiting_for_keyword)
async def film_name_step_two(message: types.Message, state: FSMContext):
    keyword = message.text
    results = read_content_according_keyword(keyword)
    await message.answer(f'<strong>{results}</strong>', parse_mode='html', reply_markup=b1)
    await state.clear()


@dp.callback_query(F.data == 'genre')
async def genre_step_one(callback: CallbackQuery):
    await callback.answer('Вы выбрали поиск по жанру')
    await callback.message.answer(f"<strong>Выберите жанр. Вы увидите все фильмы, соответствующие выбранному жанру.</strong>", reply_markup = await button_from_genres(), parse_mode='html')
@dp.callback_query(lambda call: call.data.startswith(GENRE_PREFIX))
async def genre_step_two(callback_query: CallbackQuery):
    try:
        genre = callback_query.data[len(GENRE_PREFIX):]
        results = read_content_according_genre(genre)
        await bot.send_message(callback_query.from_user.id, f'<strong>{results}</strong>', parse_mode='html', reply_markup=b1)
    except:
        await bot.send_message(callback_query.from_user.id, f'<strong>Не удалось соединиться с базой данных, перезапустите бота</strong>', parse_mode='html', reply_markup=b1)


@dp.callback_query(F.data == 'year')
async def year_step_one(callback: CallbackQuery):
    await callback.answer('Вы выбрали поиск по году релиза')
    await callback.message.answer(f'<strong>Сейчас мы будет выбирать фильмы по году релиза. Сначала мы выберем подходящий знак сравнения, а потом год.</strong>', reply_markup=b3, parse_mode='html')
@dp.callback_query(lambda call: call.data.startswith(S_PREFIX))
async def year_step_two(callback_query: CallbackQuery, state: FSMContext):
    sign= callback_query.data[len(S_PREFIX):]
    await state.update_data(s_prefix_sign=sign)
    await state.set_state(FilmSearch.s_prefix_year)
    await bot.send_message(callback_query.from_user.id, f'<strong>Теперь введите год:</strong>', parse_mode='html')
@dp.message(FilmSearch.s_prefix_year)
async def year_step_three(message: types.Message, state: FSMContext):
    await state.update_data(s_prefix_year=message.text)
    data = await state.get_data()
    try:
        result = read_content_according_year(data['s_prefix_sign'], data['s_prefix_year'])
        await message.answer(f'<strong>{result}</strong>', parse_mode='html', reply_markup=b1)
    except:
        await message.answer(f'<strong>Не удалось соединиться с базой данных, перезапустите бота</strong>', parse_mode='html', reply_markup=b1)
    finally:
        await state.clear()


@dp.callback_query(F.data == 'year_and_genre')
async def year_and_genre_step_one(callback: CallbackQuery):
    await callback.message.answer(f'<strong>Выберете знак сравнения:</strong>', reply_markup = b4, parse_mode='html')
@dp.callback_query(lambda call: call.data.startswith(M_PREFIX))
async def year_and_genre_step_two(callback_query: CallbackQuery, state: FSMContext):
    m_sign= callback_query.data[len(M_PREFIX):]
    await state.update_data(sign=m_sign)
    await state.set_state(FilmSearch.year)
    await bot.send_message(callback_query.from_user.id, f'<strong>Введите год:</strong>', parse_mode='html')
@dp.message(FilmSearch.year)
async def year_and_genre_step_three(message: types.Message, state: FSMContext):
    await state.update_data(year=message.text)
    await message.answer(f'<strong>Выберите жанр:</strong>', reply_markup = await button_from_genres_and_year(), parse_mode='html')
@dp.callback_query(lambda call: call.data.startswith(Y_PREFIX))
async def year_and_genre_step_four(callback_query: CallbackQuery, state: FSMContext):
    genre_from_button = callback_query.data[len(Y_PREFIX):]
    await state.update_data(genre = genre_from_button)
    data = await state.get_data()
    try:
        result = read_content_according_genre_and_year(data['sign'], data['year'], data['genre'])
        await bot.send_message(callback_query.from_user.id, f'<strong>{result}</strong>', parse_mode='html', reply_markup=b1)
    except:
        await bot.send_message(callback_query.from_user.id, f'<strong>Не удалось соединиться с базой данных, перезапустите бота</strong>', parse_mode='html', reply_markup=b1)
    finally:
        await state.clear()


@dp.callback_query(F.data == 'popular')
async def most_popular_films(callback: CallbackQuery):
    await callback.answer(f"Вы выбрали пункт: 'Посмотреть самые популярные запросы'")
    try:
        result = read_the_most_popular_logs()
        await callback.message.answer(f'<strong>{result}</strong>', parse_mode='html', reply_markup=b1)
    except:
        await callback.message.answer(f'<strong>Не удалось соединиться с базой данных, перезапустите бота</strong>', parse_mode='html', )


@dp. message (F.text == 'Перезапустить бота')
async def how_are_you (message: Message):
    await cmd_start(message)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass