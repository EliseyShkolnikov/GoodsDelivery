import random
import io
import requests

import vk_api
from vk_api.longpoll import *
from vk_api.keyboard import *
from vk_api.utils import get_random_id

# --
from vk_bot import VkBot
# --

num = 0
def write_msg(user_id, message):
    num = bot.update_board()
    vk.method('messages.send', {
              'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048), 'keyboard': StayHomeKeyboard(num)})


def StayHomeKeyboard(a):
    keyboard = VkKeyboard(one_time=False)
    if a == 0:
        keyboard.add_button('Курьер', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Работодатель', color=VkKeyboardColor.POSITIVE)
    elif a == 1:
        keyboard.add_button(['👉🏿', '👉🏻'][random.randint(0, 1)], color=VkKeyboardColor.DEFAULT)
        keyboard.add_button(['👍🏿', "👍🏻"][random.randint(0, 1)], color=VkKeyboardColor.DEFAULT)
        keyboard.add_line() 
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    elif a == 2:
        keyboard.add_button('Подтверждаю', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()  # Переход на четвертую строку
        keyboard.add_location_button()
        keyboard.add_line() 
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


# API-ключ созданный ранее
token = "b1652a5628af75bb7a91fd5cb0b47aae8699a941ad25c637ad6573ca49c157f722036e551983aca45fdd1"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
vk_to_use_pic = vk.get_api()
# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")
    
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print(f'New message from vk.com/id{event.user_id}', end='')
            bot = VkBot(event.user_id)
            if event.text == "":
                pass
            else:
                write_msg(event.user_id, bot.new_message(event))
            if "'attach1_type': 'photo'" in str(event.attachments):
                msg = vk_to_use_pic.messages.getById(message_ids=event.message_id)
                photo_url = str(msg['items'][0]['attachments'][0]['photo']['sizes']).split("'type':")[-1].split()[2][1:-2]
                bot.take_pic_from_Main(photo_url)
                print('Photo attach ' + photo_url)
            if event.text:
                print(f"Text - {event.text}")
            print("-------------------")
