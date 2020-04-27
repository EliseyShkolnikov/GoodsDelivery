import requests
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def get_address(address):
    URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU"
    result = requests.get(URL).json()
    print(result['response']['GeoObjectCollection']['featureMember']
          [0]['GeoObject']['boundedBy']['Envelope'])


get_address('Череповец, Олимпийская 11')


'https://yandex.ru/maps/968/cherepovets/?ll=38.023659%2C59.115075&mode=routes&rtext=~59.119678%2C38.026887&rtt=auto&ruri=~ymapsbm1%3A%2F%2Forg%3Foid%3D1206838719&z=13.88'
