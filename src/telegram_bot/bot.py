import dotenv
import telebot

from src.config import API_TOKEN
from utils import session

bot = telebot.TeleBot(API_TOKEN)

print(f'[+] bot <{bot.get_my_name().name}> started')

user_data = {}


@bot.message_handler(commands=['private'])
def get_reg(message):
    if message.from_user.id == 614437771:
        print(f'Admin enter: {message.from_user}')
        mess = session()
        bot.send_message(message.from_user.id, mess)
    else:
        bot.send_message(message.from_user.id, "Я тебя не знаю")


@bot.message_handler(content_types=['text'])
def start_message(message):
    mess = 'Я еще глупенький. Ничем не могу помочь('
    bot.send_message(message.from_user.id, mess)


# @bot.message_handler(commands=['da'])
# def get_reg(message):
#     if message.from_user.id == 614437771 or message.from_user.id == 434121417 or message.from_user.id == 857406049 or message.from_user.id == 808907061:
#         print(f'Admin enter: {message.from_user}')
#         user_data[message.from_user.id] = {}
#         bot.send_message(message.from_user.id, "Имя?")
#         bot.register_next_step_handler(message, get_name)
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не знаю")
#
#
# def get_name(message):
#     user_data[message.from_user.id]['name'] = message.text.capitalize()
#     bot.send_message(message.from_user.id, "Фамилия?")
#     bot.register_next_step_handler(message, get_surname)
#
#
# def get_surname(message):
#     user_data[message.from_user.id]['last_name'] = message.text.capitalize()
#     bot.send_message(message.from_user.id, 'Отчество?')
#     bot.register_next_step_handler(message, get_first_num_corp)
#
#
# def get_first_num_corp(message):
#     user_data[message.from_user.id]['surname'] = message.text.capitalize()
#     bot.send_message(message.from_user.id, 'Первая цифра в номере корпуса?')
#     bot.register_next_step_handler(message, get_second_num_corp)
#
#
# def get_second_num_corp(message):
#     user_data[message.from_user.id]['first_corp_number'] = message.text.capitalize()
#     bot.send_message(message.from_user.id, 'Вторая цифра в номере корпуса?')
#     bot.register_next_step_handler(message, get_done)
#
#
# def get_done(message):
#     user_data[message.from_user.id]['second_corp_number'] = message.text.capitalize()
#     temp_user = user_data[message.from_user.id]
#     print(temp_user)
#     answer = f"{temp_user['name']} {temp_user['last_name']} {temp_user['surname']} переезжает в корпус " \
#              f"{temp_user['first_corp_number']}. {temp_user['second_corp_number']}? [да/нет]"
#
#     bot.send_message(message.from_user.id, answer)
#     bot.register_next_step_handler(message, get_accept)
#
#
# def get_accept(message):
#     if message.text.capitalize().lower() == "да":
#         bot.send_message(message.from_user.id, 'Принято! Ожидай...')
#         url_ = session(user_data[message.from_user.id])
#         print(url_)
#         bot.send_message(message.from_user.id, f'Держи! {url_}')
#     elif message.text.capitalize().lower() == "нет":
#         bot.send_message(message.from_user.id, "Тогда начинай заново")
#     else:
#         bot.send_message(message.from_user.id, 'Не можешь правильно написать Да или Нет??')
#         bot.register_next_step_handler(message, get_accept)


bot.polling(none_stop=True)
