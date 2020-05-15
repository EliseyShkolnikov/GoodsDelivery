import bs4 as bs4
import sqlite3
import requests
import os.path
import io
from urllib.request import Request, urlopen
import test

import vk_api
# from vk_api.longpoll import *
# from vk_api.keyboard import *
from vk_api.utils import get_random_id


token = "b1652a5628af75bb7a91fd5cb0b47aae8699a941ad25c637ad6573ca49c157f722036e551983aca45fdd1"
vk = vk_api.VkApi(token=token)
class VkBot:
    global second_flag_to_debug
    second_flag_to_debug = False
    global text_notification
    global id_notification
    text_notification = ''
    id_notification = ''
    def __init__(self, user_id):
        self.API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
        print("\nСоздан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "КУРЬЕР", "РАБОТОДАТЕЛЬ", "ПОКА"]
        global Flaag
        Flaag = False
        # global first_flag_to_debug
        # first_flag_to_debug = False

    # Like shitcode?
    def take_pic_from_Main(self, pic_url):
        global picture
        picture = pic_url
    # Like shitcode?

    def create_new_in_GG(self, dannye):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Goods.db")
        with sqlite3.connect(db_path) as db:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO GG (Name, ID_user, Address, Address_log, Goods, Period, Coment, Photo, Condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (f"{dannye[1]} vk.com/id{self._USER_ID}", f"vk.com/id{self._USER_ID}", dannye[2], str(test.Map.get_address(dannye[2])), dannye[3], dannye[4], dannye[5], dannye[6], "Принят на сервере"))
            conn.commit()
            conn.close()
        
    def create_new_in_Goods_processed(self, dannye):
        global cond
        cond = 1
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Goods_In_processing.sqlite")
        with sqlite3.connect(db_path) as db:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Goods_processed (ID_from_GG, Who_took, recipient) VALUES (?, ?, ?)''', (dannye[0], dannye[1], dannye[2]))
            conn.commit()
            conn.close()
        self.update_condition_order_GG(dannye[0], cond)
    
    def update_condition_order_GG(self, ID, cond):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "Goods.db")
        with sqlite3.connect(db_path) as db:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            print(f"{cond} - кондитион")
            if cond == 1:
                cursor.execute(f'''UPDATE GG SET Condition = "Курьер принял ваш заказ" WHERE ID = {int(ID)}''')
                conn.commit()
            elif cond == 2:
                cursor.execute(f'''UPDATE GG SET Condition = "Курьер подъехал к вам" WHERE ID = {int(ID)}''')
                conn.commit()
            conn.close()



    def get_address(self, address):
        URL = f"https://geocode-maps.yandex.ru/1.x/?apikey={self.API_KEY}&geocode={lat},{lon}&format=json&sco=latlong&kind=house&results=1&lang=ru_RU"
        result = requests.get(URL).json()
        return result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, messag):
        global update_board_return
        update_board_return = 0
        message = messag.text
        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}! \nВозможные команды:\n«Курьер»\n«Работодатель»"

        # Работодатель
        elif message.upper() == self._COMMANDS[2]:
            update_board_return = 2
            return f'Супер, вы работодатель!\nСтрого следуйте форме заполнения!\n1) В первой строчке укажите номер, выданный администрацией\n2) Отправлять 1 сообщением\n3) Учитывать синктаксиз и орфографию\n4) При ошибочной отправке снова напишете «Работодатель»\n5) Подтвердить правила по ссылке \nhttps://vk.com/topic-194515327_44426909\nВ ответном сообщении напишете «Подтверждаю»'

        elif message.upper() == 'ПОДТВЕРЖДАЮ':
            update_board_return = 4
            return f'Сообщение начните со слова «Товар»\n1) ФИО\n2) Полный адрес\n3) Наименование товара\n4) Период размещения(день, неделя, месяц, год, навсегда)\n5) Комментарий курьеру\n6) Приложите фото товара'
        
        elif 'ТОВАР' in str(message.upper()):
            update_board_return = 2
            if len(message.split('\n')) != 6:
                return f"""1) Нужно вводить все данные по 1 строке на элемент
                           2) Скорее всего, вы не ввели один из пунктов"""
            else:
                perem = message.split('\n')
                perem.append(str(picture))
                self.create_new_in_GG(perem)
                return f"Ваш заказ принят"


        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        # Курьерская часть программы
        elif message.upper() == self._COMMANDS[1]:
            update_board_return = 1
            return f"Супер, вы курьер! Чтобы посмотреть заказы, нажмите «👉🏻»"

        # Курьер получает заказ
        elif message == '👉🏿' or message == '👉🏻' or message == '👉':
            try:
                update_board_return = 1
                global first_flag_to_debug
                global second_flag_to_debug
                first_flag_to_debug = True
                second_flag_to_debug = False
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(BASE_DIR, "Goods.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM GG WHERE Condition="Принят на сервере" ORDER BY RANDOM() LIMIT 1 ')
                results1 = cursor.fetchall()
                global results
                results = "'".join(str(results1)[2:-2].split("'")).split(',')
                conn.close()

                conn2 = sqlite3.connect(db_path)
                cursor1 = conn2.cursor()
                cursor1.execute(f'SELECT Address_log FROM GG WHERE ID = {results[0]}')
                ad_log = cursor1.fetchall()
                print(str(ad_log)[4:-5])
                conn.close()

                # Загрузка фото
                print(results[-2][2:-1])
                filedata = Request(results[-2][2:-1], headers={'User-Agent': 'Mozilla/5.0'})
                datatowrite = urlopen(filedata).read()
                with open('C:\\Users\\666\\Desktop\\GoodsDelivery\\vk_bot-master\\to_send.jpg', 'wb') as f:
                    f.write(datatowrite)
                f.close()
                # Загрузка фото
                # Подготовка к отправке фото
                print(f"{results[4]}{results[5]}".strip()[2:-2])
                first_vk_pict = vk.method('photos.getMessagesUploadServer')
                second_vk_pict = requests.post(first_vk_pict['upload_url'], files={'photo': open('C:\\Users\\666\\Desktop\\GoodsDelivery\\vk_bot-master\\to_send.jpg', 'rb')}).json()
                third_vk_pict = vk.method('photos.saveMessagesPhoto', {'photo': second_vk_pict['photo'], 'server': second_vk_pict['server'], 'hash': second_vk_pict['hash']})[0]
                to_return_pic_from_db = 'photo{}_{}'.format(third_vk_pict['owner_id'], third_vk_pict['id']).strip()
                # Подготовка к отправке фото
                print(results)
                return f"""!!!!!!\nВот и свободный заказ №{results[0]} \nИмя и вк заказчика - {results[1][2:-1].replace("'", "")} \nАдрес доставки - {results[3][2:-1].replace("'", "")} 
                    Товар - {results[7][1:-1].replace("'", "")} \n{results[9].replace("'", "")} \nЧтобы принять нажмите «👍🏻»""", to_return_pic_from_db, str(ad_log)[4:-5]
                # Курьер получает заказ
            except:
                return f"Свободных заказов, к сожалению, нет"

        elif message.upper() == 'ГОТОВО':
            if second_flag_to_debug:
                second_flag_to_debug = False
                cond = 2
                to_upload = [results[0], f"vk.com/id{self._USER_ID}", f"{results[1]}"]
                self.update_condition_order_GG(to_upload[0], cond)

                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(BASE_DIR, "Goods.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(f'SELECT ID_user FROM GG WHERE ID = {results[0]}')
                results1 = cursor.fetchall()
                global id_notification
                id_notification = results1
                conn.close()

                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(BASE_DIR, "Goods.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(f'SELECT Goods FROM GG WHERE ID = {results[0]}')
                results2 = cursor.fetchall()
                conn.close()

                global text_notification
                text_notification = f"Курьер подошел к вам по заказу - {str(results2)[3:-4].strip()}"
                global Flaag
                Flaag = True
                return f"Клиент получил уведомление о заказе"
            else:
                return f"Вы не подтвердили заказ, чтобы нажимать 'Готово'"

        # Решение принять ли заказ
        elif message.upper() == '👍🏻' or message.upper() == '👍🏿' or message.upper() == '👍':
            try:
                if first_flag_to_debug:
                    first_flag_to_debug = False
                    second_flag_to_debug = True
                    update_board_return = 3
                    to_upload = [results[0], f"vk.com/id{self._USER_ID}", f"{results[1]}"]
                    self.create_new_in_Goods_processed(to_upload)
                    return f"Вы приняли заказ!» При выполнении доставки напишите «Готово»"
                else:
                    return f"Нельзя принять заказ, не выбрав какой заказ хотите принять"
            except:
                update_board_return = 1
                return f"Нельзя принять заказ, не выбрав какой заказ хотите принять"
        elif message.upper() == 'НАЗАД':
            update_board_return = 0
            return f"Вы вернулись на вкладку назад"
        else:
            return f"Не понимаю о чем вы...\nВозможные команды:\n«Курьер»\n«Работодатель»"
        # Решение принять ли заказ
        # Курьерская часть программы
        
    def update_board(self):
        if update_board_return == 0:
            return update_board_return
        elif update_board_return == 1:
            return update_board_return
        elif update_board_return == 2:
            return update_board_return
        elif update_board_return == 3:
            return update_board_return
        elif update_board_return == 4:
            return update_board_return

    def new_message_notification(self):
        global text_notification
        global id_notification
        global Flaag
        one = text_notification
        two = id_notification
        three = Flaag
        text_notification = ['']
        id_notification = ['']
        Flaag = False
        return [one, two, three]

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
