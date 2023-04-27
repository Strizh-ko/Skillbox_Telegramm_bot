import requests
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types

from loader import bot

import requests




def location(city):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q":city,"locale":"ru_RU","langid":"1033","siteid":"300000001"}

    headers = {
        "X-RapidAPI-Key": "dd59e05dadmsh500e1e69d3c4381p1b8760jsnc4ec1c6cf22a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)

    with open('hotels.json', 'w') as file:
        json.dump(data, file, indent=4)



    cities_dct = {}

    for loc in data['sr']:
        if loc['type'] == 'CITY':
            cities_dct[loc['regionNames']['shortName']] = loc['gaiaId']

    print(cities_dct)
    return cities_dct




def hotels(chat_id):
    with bot.retrieve_data(chat_id) as data:
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": list(data['cities_dct'].values())[0]},
            "checkInDate": {
                "day": int(data['ad']),
                "month": int(data['am']),
                "year": int(data['ay'])
            },
            "checkOutDate": {
                "day": int(data['dd']),
                "month": int(data['dm']),
                "year": int(data['dy'])
            },
            "rooms": [
                {
                    "adults": data['people'],

                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": 500,
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"price": {
                "max": 1000000,
                "min": 1
            }}
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "dd59e05dadmsh500e1e69d3c4381p1b8760jsnc4ec1c6cf22a",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

    try:
        data = requests.request("POST", url, json=payload, headers=headers)

        data = json.loads(data.text)
        hotels_lst = data["data"]["propertySearch"]["properties"]

        with open('hottels.json', 'w') as file:
            json.dump(hotels_lst, file, indent=4)

        return hotels_lst

    except:
        return None


