# -*- coding: utf-8 -*-
import os
from datetime import datetime
import constants
import telebot
import users
from telebot import types
import time
import urllib
import glob
import re
from os import path
import organization
from organization import data


bot = telebot.TeleBot(constants.token)
client_operator_chat = {}
operator_client_chat = {}
TEAM_USER_LOGGING = 0
TEAM_USER_ACCEPTED = 1
team_users = users.TeamUserList()
user_step = {}
user_chat = False
user_id = 0
print(bot.get_me())
userinn = False
mesint = False
sendmess = False
boolean = False
chatoff = False
chatoff2 = False

def get_user_step(uid):
    if uid in user_step:
        return user_step[uid]
    else:
        knownUsers.append(uid)
        user_step[uid] = 0
        return 0
#Вывод сообщений в командной строке
def log(message, answer):
    try:
        print("\n ------")
        print(datetime.now())
        print("Сообщение от " + str(message.from_user.first_name) + " " + str(message.from_user.last_name) + ". id = " + str(message.from_user.id) + ".\nID сообщения - " + str(message.message_id) + " Текст - " + str(message.text)+"")
        print("Ответ - " + answer)
    except ValueError:
        pass

# Реагирует на /start просто отдаёт приветственное сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/number', '/location')
    user_markup.row( '/dogovor', '/start')
    bot.send_message(message.chat.id, "Добро пожаловать! \nЯ бот ЦЗИ «Север».\nНажмите /dogovor если вы новый клиент. \nНажмите /number чтобы узнать номер телефона офиса. \nНажмите /location чтобы узнать адрес офиса.\nДля соединения с оператором, введите свой ИНН. ",  reply_markup=user_markup)

#Реагирует на комнанду /help и выводит сообщение
@bot.message_handler(commands=['help'])
def send_welcome(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/number', '/location')
    user_markup.row( '/dogovor', '/start', '/help')
    bot.send_message(message.chat.id, "\nНажмите /dogovor если вы новый клиент. \nНажмите /number чтобы узнать номер телефона офиса. \nНажмите /location чтобы узнать адрес офиса.\nДля соединения с оператором, введите свой ИНН.\nВы также можете отправить картинки, документы, голосовое сообщение",  reply_markup=user_markup)

# Авторизация операторов по паролю
@bot.message_handler(commands=['on'])
def login_operator(message):
    try:
        if message.chat.id in team_users:
            bot.reply_to(message, "Вы уже оператор")
        else:
            user_step[message.chat.id] = TEAM_USER_LOGGING
            bot.reply_to(message, "Введите секретный код:")
    except ValueError:
        pass

# Оператор введет пароль, чтобы авторизоваться
@bot.message_handler(func=lambda message: user_step.get(message.chat.id) == TEAM_USER_LOGGING)
def team_user_login(message):
    try:
        if message.text == 'password1': #Заменить password1 на новый пароль при смене пароля
            team_users.add(users.TeamUser(message.chat.id))
            user_step[message.chat.id] = TEAM_USER_ACCEPTED
            print(user_step[message.chat.id])
            bot.reply_to(message, "Вы уже можете принимать сообщение, как оператор")
            answer = 'Новый оператор'
            log(message, answer)
        else:
            user_step[message.chat.id] = 1
            bot.reply_to(message, "Не правильно ввели пароль, повторите сначала набрать команду /on")
    except ValueError:
        pass

# Команда, по которой удаляешься из списка операторов
@bot.message_handler(commands=['off'])
def team_user_logout(message):
    try:
        if message.chat.id not in team_users:
            bot.reply_to(message, "Вы уже не оператор:(")
        else:
            team_users.remove_by_chat_id(message.chat.id)
            bot.reply_to(message, "Вы прекратили отвечать на сообщение")

        answer = 'Оператор отключился'
        log(message, answer)
    except ValueError:
        pass

#Команда составление новых договоров(новые клиенты)
@bot.message_handler(commands=['dogovor'])
def location_command(message):
    for user in team_users:
        global sendmess
        global user_chat, userinn, boolean, chatoff, count1

        bot.send_message(user.chat_id, 'Клиент {name} с номером чата /chat_{client_chat_id} хочет заключить новый договор'.format(
        name=str(message.from_user.first_name), client_chat_id=str(message.chat.id)))

        sendmess = True
        user_chat = True
        userinn = True
        boolean = False
        chatoff = False
        count1 = False

        print("dog user chat", user_chat)
        print("dog sendmes", sendmess)
    answer = 'Ожидайте ответ оператора'
    log(message, answer)
            #bot.send_chat_action(message.chat.id, 'find_location')
    bot.send_message(message.chat.id, answer)


# Команда показываюшая адрес офиса
@bot.message_handler(commands=['location'])
def location_command(message):
    answer = 'Отправка локации'
    log(message, answer)
    bot.send_chat_action(message.chat.id, 'find_location')
    bot.send_venue(message.chat.id, 62.030357, 129.762587, "ЦЗИ Север", "Ларионова, 10")

#Команда показывает номер телефона
@bot.message_handler(commands=['number'])
def location_command(message):
    answer = 'Номер телефона (4112) 390095, 390096, 219393'
    log(message, answer)
    #bot.send_chat_action(message.chat.id, 'find_location')
    bot.send_message(message.chat.id, answer)


# Позволяет оператору выбрать чат с каким клиентом общаться
@bot.message_handler(regexp='\/chat_\d*$')
def set_chat_operator_to_client(message):
    global user_chat
    global user_id
    try:
        client_operator_chat[message.chat.id] = users.message_num(message.text)
        bot.send_message(int(client_operator_chat[message.chat.id]), 'Здравствуйте, оператор подключен, ждем ваш вопрос')

        for user in team_users:
            if message.chat.id == int(user.chat_id):
                continue
            else:
                bot.send_message(user.chat_id,
                         'Оператор {name} обслуживает клиента '
                         ':\n{msg_text}'.format(
                                              name=str(message.from_user.first_name),
                                              msg_text=message.text))
        user_id = message.chat.id

        user_chat = True
    except ValueError:
        pass

now_time = datetime.now()
cur_hour = now_time.hour
print(cur_hour)

# Проверка по инн. Если инн введен верно, то отправляет сообщение всем операторам, и если оператор выбрал чат, то начинается переписка сообщений. Если нет выводит сообщение неверный ввод инн
@bot.message_handler(func=lambda message: users.client_operator(message.chat.id))
def chat_with_operator(message):
    global user_chat
    global client_operator_chat
    global user_id
    global data
    global userinn, mesint
    global sendmess, boolean, chatoff, chatoff2
    count = 0
    count1 = 0
    if(9 <= cur_hour < 18):
        try:
            if(mesint == False):
                for i in data:

                    if message.text == i['inn']:
                        userinn = True
                        count1 = count1 + 1

                        for user in team_users:
                            if user_chat is False and count1 == 1:
                                bot.send_message(user.chat_id,  'Клиент {name} с номером чата /chat_{client_chat_id} c инн {inn} написал(а):\n{msg_text}'.format(
                                name=str(message.from_user.first_name), client_chat_id=str(message.chat.id), msg_text=message.text, inn=i['inn']))
                                chatoff2 = True
                                print(i)
                    if message.text != i['inn']:
                        count = count + 1
                        boolean = True
                    if message.text == i:
                        print("sdsdsd")
                if(boolean == True and userinn == False):
                    bot.reply_to(message, "Вы не верно ввели ИНН или не являетесь нашим клиентом. Пожалуйста, удостовертесь в правильном вводе ИНН.")
                if(chatoff == True and count1 != 1):
                    bot.reply_to(message, "Вы не верно ввели ИНН или не являетесь нашим клиентом. Пожалуйста, удостовертесь в правильном вводе ИНН.")
                print(message.text)


            if userinn is True:
                if user_chat is False and count1 == 1:
                    sendmess = True

                if(count1 == 1):
                    bot.reply_to(message, "Ожидайте ответ оператора")

                if user_chat is True and sendmess == True:

                    try:
                        bot.send_message(user_id,  '{name} с номером чата /chat_{client_chat_id}  написал(а):\n{msg_text}'.format(
                        name=str(message.from_user.first_name), client_chat_id=str(message.chat.id), msg_text=message.text))
                        mesint = True
                    except ValueError:
                        pass
        except ValueError:
            pass

         # добавляет всех новых операторов в словарь и значение None
            answer = "клиент"
            log(message, answer)
        except ValueError:
            pass
    else:
        print("Извините, техническая поддержка работает с 9:00 до 18:00, с перерывом на обед с 13:00-14:00. Пожалуйста обратитесь завтра")




#Отправка картинок, фото от лица клиента
@bot.message_handler(content_types=['photo'], func=lambda message: users.client_operator(message.chat.id))
def send_clientphoto(message):
    global user_chat
    global client_operator_chat
    global user_id
    global userinn, sendmess

    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)

    try:
        if user_chat == True and sendmess == True:

            try:
                bot.send_photo(user_id, file_id)
            except ValueError:
                pass
    except ValueError:
        pass
#Отправка голосовых сообщений от лица клиента
@bot.message_handler(content_types=['voice'], func=lambda message: users.client_operator(message.chat.id))
def send_clientvoice(message):
    global user_chat
    global client_operator_chat
    global user_id
    global userinn, sendmess

    file_id = message.voice.file_id
    path = bot.get_file(file_id)

    if user_chat is True and sendmess is True:

        try:
            #bot.send_photo(int(client_operator_chat[user.chat.id]), file_id)
            bot.send_voice(user_id, file_id)
        except ValueError:
            pass
#отправка документов от лица клиента
@bot.message_handler(content_types=['document'], func=lambda message: users.client_operator(message.chat.id))
def send_clientdoc(message):
    global user_chat
    global client_operator_chat
    global user_id, sendmess

    file_id = message.document.file_id
    path = bot.get_file(file_id)

    if user_chat is True and sendmess is True:
        try:
            #bot.send_photo(int(client_operator_chat[user.chat.id]), file_id)
            bot.send_document(user_id, file_id)
        except ValueError:
            pass


#Отключение чата с клиентом
@bot.message_handler(regexp='\/chat_\off', func=lambda message: not users.client_operator(message.chat.id))
def set_chat_operator_to_client(message):
    global user_chat
    global mesint
    global chatoff

    bot.send_message(int(client_operator_chat[message.chat.id]), 'Оператор закончил общение с вами. Чтобы обратиться к нам нажмите /start')
    try:
        client_operator_chat[message.chat.id] = None
        for user in team_users:
            if message.chat.id == int(user.chat_id):
                continue
            else:
                bot.send_message(user.chat_id,
                         'Оператор {name} закончил обслуживать клиента '
                         ':\n{msg_text}'.format(
                                              name=str(message.from_user.first_name),
                                              msg_text=message.text))

        user_chat = False
        mesint = False
        chatoff = True

    except ValueError:
        pass


# Смотрит с кем выбрал общаться оператор и направляет сообщения от оператора - клиенту
@bot.message_handler(func=lambda message: not users.client_operator(message.chat.id))
def chat_with_client(message):
    try:
        if client_operator_chat[message.chat.id] is None:
            bot.send_message(message.chat.id,
                             'для ответа нужному клиенту, необходимо нажать над его сообщением на /chat_...')
        else:
            bot.send_message(int(client_operator_chat[message.chat.id]), message.text)
            print(int(client_operator_chat[message.chat.id]))
            for user in team_users:
                if message.chat.id == int(user.chat_id):
                    continue

    except KeyError:
        bot.send_message(message.chat.id, 'клиент ещё ничего не писал')
    answer = 'Оператор'
    log(message,answer)

#отправка фото, картинок от лица оператора
@bot.message_handler(content_types='photo', func=lambda message: not users.client_operator(message.chat.id))
def photo_with_client(message):
    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)

    try:
        if client_operator_chat[message.chat.id] is None:
            bot.send_message(message.chat.id,
                             'для ответа нужному клиенту, необходимо нажать над его сообщением на /chat_...')
        else:
            bot.send_photo(int(client_operator_chat[message.chat.id]), file_id)
            print(int(client_operator_chat[message.chat.id]))

            for user in team_users:
                if message.chat.id == int(user.chat_id):
                    continue

    except KeyError:
        bot.send_message(message.chat.id, 'клиент ещё ничего не писал')
    answer = 'Оператор'
    log(message,answer)
#отправка документов от лица оператора
@bot.message_handler(content_types='document', func=lambda message: not users.client_operator(message.chat.id))
def doc_with_client(message):
    file_id = message.document.file_id
    path = bot.get_file(file_id)

    try:
        if client_operator_chat[message.chat.id] is None:
            bot.send_message(message.chat.id,
                             'для ответа нужному клиенту, необходимо нажать над его сообщением на /chat_...')
        else:
            bot.send_document(int(client_operator_chat[message.chat.id]), file_id)

            for user in team_users:
                if message.chat.id == int(user.chat_id):
                    continue

    except KeyError:
        bot.send_message(message.chat.id, 'клиент ещё ничего не писал')
    answer = 'Оператор'
    log(message,answer)
#отправка голосовых сообщений от лица оператора
@bot.message_handler(content_types='voice', func=lambda message: not users.client_operator(message.chat.id))
def voice_with_client(message):
    file_id = message.voice.file_id
    path = bot.get_file(file_id)

    try:
        if client_operator_chat[message.chat.id] is None:
            bot.send_message(message.chat.id,
                             'для ответа нужному клиенту, необходимо нажать над его сообщением на /chat_...')
        else:
            bot.send_voice(int(client_operator_chat[message.chat.id]), file_id)

            for user in team_users:
                if message.chat.id == int(user.chat_id):
                    continue

    except KeyError:
        bot.send_message(message.chat.id, 'клиент ещё ничего не писал')
    answer = 'Оператор'
    log(message,answer)

# Запуск бота, стараемся не обращать внимания на ошибки
if __name__ == '__main__':
    bot.polling(none_stop=True)
