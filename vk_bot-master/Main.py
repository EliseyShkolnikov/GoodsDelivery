import random

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
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Курьер', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Работодатель', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('👉🏿', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Подтверждаю', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()  # Переход на третью строку
    keyboard.add_button('👍🏿', color=VkKeyboardColor.DEFAULT)
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

        if event.to_me:

            print(f'New message from {event.user_id}', end='')

            bot = VkBot(event.user_id)

            if event.text[0] == "/":
                write_msg(event.user_id)
            else:
                write_msg(event.user_id, bot.new_message(event.text))

            print('Text: ', event.text)
            print("-------------------")
