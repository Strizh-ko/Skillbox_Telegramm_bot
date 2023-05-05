import os
from datetime import datetime
from loader import bot


def save(chat_id):
    with bot.retrieve_data(chat_id) as data:
        text = f"Запрос от {datetime.now()}: {data['command']}\n" \
               f"{data['search_param_text']}"

    if os.listdir('./database/history'):
        with open(f'./database/history/{chat_id}.txt', 'r', encoding="utf-8") as file:
            lst = file.read().split('\n\n')
            if len(lst) >= 5:
                lst.pop(0)
            lst.append(text)
    else:
        lst = [text]
    with open(f'./database/history/536000640.txt', 'w', encoding="utf-8") as file:
        file.write('\n\n'.join(lst))


def view(chat_id):
    with open(f'./database/history/{chat_id}.txt', 'r', encoding="utf-8") as file:
        lst = file.read().split('\n\n')
        for req in lst:
            bot.send_message(chat_id, req)
