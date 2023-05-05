def filter(command: str, hotels_lst: list, quant: int):
    if command == '/lowprice':
        hotels_lst.sort(key=lambda dct: dct['price'])

    elif command == '/highprice':
        hotels_lst.sort(key=lambda dct: dct['price'], reverse=True)

    selected_hotels = hotels_lst[0:quant]
    return selected_hotels


def bd_filter(hotels_lst: list, quant: int, price: int, distance: float):
    filter_hotels = []
    for hotel in hotels_lst:
        if hotel['price'] <= price and hotel['distance'] <= distance:
            filter_hotels.append(hotel)

    filter_hotels.sort(key=lambda dct: dct['bestdeal'])

    selected_hotels = filter_hotels[0:quant]
    return selected_hotels
