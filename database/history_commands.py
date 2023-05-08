import os
from datetime import datetime
from loader import bot
import sqlite3 as sql



def save(chat_id):
    create_db(chat_id)
    hist_path = f'{os.sep}'.join(['.', 'database', 'history.db'])
    with sql.connect(hist_path) as con:
        cur = con.cursor()
        with bot.retrieve_data(chat_id) as data:
            if data['command'] != '/bestdeal':
                data['price'] = 'NULL'
                data['distance'] = 'NULL'
            cur.execute(f"INSERT INTO h_{chat_id} (date, command, city, a_date, d_date, people, price, distance)"
                        f"VALUES ("
                        f"'{str(datetime.now())[0:19]}',"
                        f"'{data['command']}',"
                        f"'{list(data['cities_dct'].items())[0][0]}',"
                        f"'{data['a_date']}',"
                        f"'{data['d_date']}',"
                        f"{data['people']},"
                        f"{data['price']},"
                        f"{data['distance']})")


def view(chat_id):
    hist_path = f'{os.sep}'.join(['.', 'database', 'history.db'])
    with sql.connect(hist_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM h_{chat_id}")
        result = cur.fetchall()
        if len(result) == 0:
            bot.send_message(chat_id, 'История пуста')
        else:
            for note in result:
                req = f'Запрос от {note[0]}: {note[1]}\n' \
                      f'Город назначения: {note[2]}\n'\
                      f'Дата прибытия: {note[3]}\n'\
                      f'Дата отбытия: {note[4]}\n'\
                      f'Количество человек: {note[5]}\n'
                if note[1] == '/bestdeal':
                    req += f'Максимальная цена: {note[6]}\n' \
                           f'Максимальная дистанция до центра: {note[7]}'
                bot.send_message(chat_id, req)


def create_db(chat_id):
    with sql.connect('./database/history.db') as con:
        cur = con.cursor()

        cur.execute(f"""CREATE TABLE IF NOT EXISTS h_{chat_id} (
            date TEXT,
            command TEXT,
            city TEXT,
            a_date TEXT,
            d_date TEXT,
            people INTEGER,
            price INTEGER,
            distance REAL
            )""")