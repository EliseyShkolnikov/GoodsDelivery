import random
import io
import requests

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

# --
from vk_bot import VkBot
# --


def write_msg(user_id, message):
    vk.method('messages.send', {
              'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048), 'keyboard': StayHomeKeyboard()})


def StayHomeKeyboard():
    print(random.randint(1, 2))
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Курьер', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Работодатель', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button(['👉🏿', '👉🏻'][random.randint(0, 1)], color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Подтверждаю', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()  # Переход на третью строку
    keyboard.add_button(['👍🏿', "👍🏻"][random.randint(0, 1)], color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Товар', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()  # Переход на четвертую строку
    keyboard.add_location_button()
    return keyboard.get_keyboard()


# API-ключ созданный ранее
token = "b1652a5628af75bb7a91fd5cb0b47aae8699a941ad25c637ad6573ca49c157f722036e551983aca45fdd1"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")

    
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print(event.attachments)
        if event.to_me:
            print(f'New message from vk.com/id{event.user_id}', end='')
            bot = VkBot(event.user_id)
            if event.text == "":
                pass
            else:
                write_msg(event.user_id, bot.new_message(event.text))
            if 'photo' in str(event.attachments):
                print('Photo attach - vk.com/photo' + event.attachments['attach1'])
            if event.text:
                print(f"Text - {event.text}")
            print("-------------------")
