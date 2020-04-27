import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from commander.commander import Commander


def write_msg(user_id, message):
    vk.method('messages.send', {
              'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


# API-ключ созданный ранее
token = "b1652a5628af75bb7a91fd5cb0b47aae8699a941ad25c637ad6573ca49c157f722036e551983aca45fdd1"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Commander
commander = Commander()

print("Бот запущен")
# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text

            # Каменная логика ответа
            if request == "привет":
                write_msg(event.user_id, "Хай")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request.split()[0] == "command":
                write_msg(event.user_id, commander.do(request[8::]))
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
