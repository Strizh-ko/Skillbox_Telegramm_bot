import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("lowprice", 'Поиск бюджетных отелей'),
    ('highprice', 'Поиск дорогих отелей'),
    ('bestdeal', 'Поиск лучшему соотношению цена/расположение'),
    ("help", "Вывести справку"),
    ("history", "Посмотреть последние 5 запросов"),
)


