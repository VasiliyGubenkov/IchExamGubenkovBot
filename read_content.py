import mysql.connector
from logger import *

password = {'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
            'user': 'ich1',
            'password': ' ',
            'database': 'sakila'}

base_request = """SELECT film.title,
                                category.name as 'category',
                                film.description,
                                film.release_year, 
                                language.name AS language, 
                                film.length AS 'length(min)'
                            FROM film
                            JOIN language
                            ON film.language_id = language.language_id
                            JOIN film_category
                            ON film.film_id = film_category.film_id
                            JOIN category
                            ON film_category.category_id = category.category_id"""


def read_content_according_keyword(x):
    connection = mysql.connector.connect(**password)
    cursor = connection.cursor()
    cursor.execute(f""" {base_request} WHERE film.title LIKE %s """, (('%' + x + '%'),))
    rows = cursor.fetchall()
    back_all = ""
    if rows:
        headers = [desc[0] for desc in cursor.description]
        for row in rows:
            for header, value in zip(headers, row):
                back_all += f"{header}: {value}\n"
            back_all += "\n"
        to_logger = f"movie title contains: {x}"
        write_log(to_logger)
    else:
        back_all += f'В базе данных отсутствуют фильмы, содержащие в названии: {x}'
    cursor.close()
    connection.close()
    return back_all


def read_content_according_genre(x):
    connection = mysql.connector.connect(**password)
    cursor = connection.cursor()
    cursor.execute(f""" {base_request} WHERE category.name LIKE %s limit 10""", (('%' + x + '%'), ))
    rows = cursor.fetchall()
    back_all = ""
    if rows:
        headers = [desc[0] for desc in cursor.description]
        for row in rows:
            for header, value in zip(headers, row):
                back_all += f"{header}: {value}\n"
            back_all += "\n"
        to_logger = f"genre: {x}"
        write_log(to_logger)
    else:
        back_all += f'В базе данных отсутствуют фильмы, содержащие в жанре: {x}'
    cursor.close()
    connection.close()
    return back_all


def read_content_according_year(sign, year):
    connection = mysql.connector.connect(**password)
    cursor = connection.cursor()
    cursor.execute(f""" {base_request} WHERE film.release_year {sign} %s limit 10""", (year, ))
    rows = cursor.fetchall()
    back_all = ""
    if rows:
        headers = [desc[0] for desc in cursor.description]
        for row in rows:
            for header, value in zip(headers, row):
                back_all += f"{header}: {value}\n"
            back_all += "\n"
        to_logger = f"year of release: {sign} {year}"
        write_log(to_logger)
    else:
        back_all += (f'В базе данных отсутствуют фильмы, {sign} {year} года')
    cursor.close()
    connection.close()
    return back_all


def read_content_according_genre_and_year(sign, year, genre):
    connection = mysql.connector.connect(**password)
    cursor = connection.cursor()
    cursor.execute(f""" {base_request} WHERE film.release_year {sign} %s and category.name = %s limit 10""", (year, genre))
    rows = cursor.fetchall()
    back_all = ""
    if rows:
        headers = [desc[0] for desc in cursor.description]
        for row in rows:
            for header, value in zip(headers, row):
                back_all += f"{header}: {value}\n"
            back_all += "\n"
        to_logger = f'year of release: {sign} {year} and genre: {genre}'
        write_log(to_logger)
    else:
        back_all += (f'В базе данных отсутствуют фильмы, содержащие в жанре: {genre}, и при этом {sign} {year} года')
    cursor.close()
    connection.close()
    return back_all


def read_all_genres():
    connection = mysql.connector.connect(**password)
    cursor = connection.cursor()
    cursor.execute("SELECT name from category;")
    rows = cursor.fetchall()
    back_all = []
    for row in rows:
        back_all.extend(row)
    cursor.close()
    connection.close()
    return back_all


def read_the_most_popular_logs():
        connection = mysql.connector.connect(**password_for_log)
        cursor = connection.cursor()
        cursor.execute("""SELECT content as Request, COUNT(*) AS Count
                            FROM log
                            GROUP BY content
                            ORDER BY count DESC
                            LIMIT 3""")
        rows = cursor.fetchall()
        back_all = ""
        if rows:
            headers = [desc[0] for desc in cursor.description]
            for row in rows:
                for header, value in zip(headers, row):
                    back_all += f"{header}: {value}\n"
                back_all += "\n"
        cursor.close()
        connection.close()
        return back_all

