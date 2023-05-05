import json
from loader import bot
import requests
from config_data.config import RAPID_API_KEY


def location(city):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = ''
    for _ in range(10):
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == requests.codes.ok:
            break

    data = json.loads(response.text)
    cities_dct = {}

    for loc in data['sr']:
        if loc['type'] == 'CITY':
            cities_dct[loc['regionNames']['shortName']] = loc['gaiaId']

    print(f'Список городов: {cities_dct}')
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
            "resultsSize": 200,
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"price": {
                "max": 1000000,
                "min": 1
            }}
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

    try:
        data = ''
        for _ in range(10):
            data = requests.request("POST", url, json=payload, headers=headers)
            if data.status_code == requests.codes.ok:
                break

        data = json.loads(data.text)
        hotels_lst = [
            {
                'id': hotel['id'],
                'name': hotel['name'],
                'distance': hotel["destinationInfo"]["distanceFromDestination"]["value"],
                'price': round(hotel["price"]["lead"]["amount"], 0),
                'total_price': hotel["price"]["displayMessages"][1]["lineItems"][0]["value"],
                'bestdeal': round(hotel["price"]["lead"]["amount"]/hotel["destinationInfo"]["distanceFromDestination"]["value"])
             }
            for hotel in data["data"]["propertySearch"]["properties"]]

        print(f'Сформирован список из {len(hotels_lst)} отелей')
        return hotels_lst
    except:
        return None


def hotels_detail(hotels: list):
    hotels_detail_lts = []
    for hotel in hotels:
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": hotel['id']
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        data = ''
        for _ in range(10):
            data = requests.post(url, json=payload, headers=headers)
            if data.status_code == requests.codes.ok:
                break

        data = json.loads(data.text)
        hotel_detail = {
                'id': data["data"]["propertyInfo"]["summary"]['id'],
                'name': data["data"]["propertyInfo"]["summary"]['name'],
                'address': data["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"],
                "images": [img["image"]["url"] for img in data["data"]["propertyInfo"]["propertyGallery"]["images"]],
                'price': hotel['price'],
                'total_price': hotel['total_price'],
                'distance': hotel['distance'],
             }
        hotels_detail_lts.append(hotel_detail)
        print(f"Детализация отеля {hotel_detail['id']} завершена")
    print(f"Сформирован список деталей по {len(hotels_detail_lts)} отелям")
    return hotels_detail_lts



