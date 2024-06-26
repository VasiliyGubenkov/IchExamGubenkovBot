from read_content import *
from logger import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage


b1 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Перезапустить бота')]],
    resize_keyboard=True)


b2 = InlineKeyboardMarkup(inline_keyboard=[
     [InlineKeyboardButton(text='По названию', callback_data='film_name', parse_mode = 'html')],
     [InlineKeyboardButton(text='По жанру', callback_data='genre')],
     [InlineKeyboardButton(text='По году релиза', callback_data='year')],
     [InlineKeyboardButton(text='По году и по жанру', callback_data='year_and_genre')],
     [InlineKeyboardButton(text='Посмотреть популярные запросы', callback_data='popular')]],
     input_field_placeholder='Выберите пункт меню')

S_PREFIX = 's_'
b3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='=', callback_data=S_PREFIX + '=')],
    [InlineKeyboardButton(text='<', callback_data=S_PREFIX + '<')],
    [InlineKeyboardButton(text='>', callback_data=S_PREFIX + '>')],
    [InlineKeyboardButton(text='<=', callback_data=S_PREFIX + '<=')],
    [InlineKeyboardButton(text='>=', callback_data=S_PREFIX + '>=')]
    ])


M_PREFIX = 'm_'
b4 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='=', callback_data=M_PREFIX + '=')],
    [InlineKeyboardButton(text='<', callback_data=M_PREFIX + '<')],
    [InlineKeyboardButton(text='>', callback_data=M_PREFIX + '>')],
    [InlineKeyboardButton(text='<=', callback_data=M_PREFIX + '<=')],
    [InlineKeyboardButton(text='>=', callback_data=M_PREFIX + '>=')]
    ])


all_genres = read_all_genres()
GENRE_PREFIX = 'genre_'
async def button_from_genres():
    x = InlineKeyboardBuilder()
    for genre in all_genres:
        x.add(InlineKeyboardButton(text=genre, callback_data=GENRE_PREFIX + genre))
    return x.adjust(1).as_markup()


Y_PREFIX = 'y_'
async def button_from_genres_and_year():
    x = InlineKeyboardBuilder()
    for y in all_genres:
        x.add(InlineKeyboardButton(text=y, callback_data=Y_PREFIX + y))
    return x.adjust(1).as_markup()

