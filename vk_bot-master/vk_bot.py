import bs4 as bs4
import sqlite3
import requests


class VkBot:

    def __init__(self, user_id):
        self.API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
        print("\nСоздан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "КУРЬЕР", "РАБОТОДАТЕЛЬ", "ПОКА"]

    def create_new(self, s):
        conn = sqlite3.connect('Goods.db')
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO Goods(Name, Address, Goods, Period, Coment, Photo, ID) VALUES (?, ?, ?, ?, ?, ?, ?)''', (s[1], s[2], s[3], s[4], s[5], s[6], '1'))
        conn.commit()
        conn.close()


    def get_address(address):
        URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={self.API_KEY}&geocode={lat},{lon}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU"
        result = requests.get(URL).json()
        return result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}! \nВозможные команды:\n«Курьер»\n«Работодатель»"

            # Работодатель
        elif message.upper() == self._COMMANDS[2]:
            return f'Супер, вы работодатель!\nСтрого следуйте форме заполнения!\n1) В первой строчке укажите номер, выданный администрацией\n2) Отправлять 1 сообщением\n3) Учитывать синктаксиз и орфографию\n4) При ошибочной отправке снова напишете «Работодатель»\n5) Подтвердить правила по ссылке \nhttps://vk.com/topic-194515327_44426909\nВ ответном сообщении напишете «Подтверждаю»'

        elif message.upper() == 'ПОДТВЕРЖДАЮ':
            return f'Сообщение начните со слова «Товар»\n1) ФИО\n2) Полный адрес\n3) Наименование товара\n4) Период размещения(день, неделя, месяц, год, навсегда)\n5) Коментарий курьеру\n6) Ссылка на фотографию товара'

        elif str(message.upper())[0: 5] == 'ТОВАР':
            s = message.split()
            # return message
            return self.create_new(s)

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        # Курьер
        elif message.upper() == self._COMMANDS[1]:
            return f"Супер, вы курьер! Чтобы посмотреть заказы, нажмите «👉🏻»"

        elif message == '👉🏿' or message == '👉🏻' :
            conn = sqlite3.connect('Goods.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Goods")
            results1 = cursor.fetchall()
            results = "'".join(str(results1)[2:-2].split("'")).split(',')
            return f"!!!!!!\nВот и {results[6]} заказ \nИмя заказчика - {results[0][1:-1]} \nКуда доставлять - {results[1][2:-1]} \nТовар - {results[2][2:-1]} \n{results[5][:-1]} \nЧтобы принять нажмите «👍🏻»"
            conn.close()
        elif message.upper() == '👍🏻' or message.upper() == '👍🏿':
            return f"Вы приняли заказ!» При выполнении доставки напишите «Готово»"
        else:
            return f"Не понимаю о чем вы...\nВозможные команды:\n«Курьер»\n«Работодатель»"
    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result
