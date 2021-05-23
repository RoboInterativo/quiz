#!# -*- coding: utf-8 -*-
# This module provides quiz game for  Telegram Bot using
# official python-telegram-bot library
# Copyright (C) 2021
# RoboInterativo  <info@robointerativo>
# Aleksey Shilo  <alex.pricker@gmail.com>
# for information use this bot https://web.telegram.org/#/im?p=@robointerativobot
# Данный модуль позволяет заапустить бот викторину в Telegram
# использует официальную библиотеку python-telegram-bot library
# Copyright (C) 2021
# RoboInterativo  <info@robointerativo>
# Алексей Шило  <alex.pricker@gmail.com>
# Для справок используйте бот  https://web.telegram.org/#/im?p=@robointerativobot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from gettext import gettext as _
import os
import sys
import logging
import random
import yaml
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import setup








state_bot = {'tries': 0, 'quest': False, 'q': {}}

#os.environ.get('TOKEN')
setup.set_up()
LANG = os.environ['LANGUAGE']
print(LANG)
HELP_MESSAGE = _('''
Этот бот позволяет играть в викторину,     аналог trivia .
Разработан в рамках обучающего курса программирования python,
проекта https://wiki.robointerativo.ru
Автор бота: Алексей Шило AKA Alexpricker, AKA chiefexb,
Актуальная версия бота доступна по ссылке https://github.com/RoboInterativo/quiz
Узнать об обучающем проекте можно у бота @roboInterativobot
Доступные команды
/ask Начать играть.
/help эта комманда

Запусти викторину /ask
''')

with open('./config.yml', 'w') as f:

    if os.environ.get('TOKEN') != None:
        config = {'token': os.environ.get('TOKEN')}
        f.write(yaml.dump(config))
        f.close()
    else:

        print(_('''
        Не установлена переменная TOKEN
        для ее установки Набери
        export TOKEN=TOKEN_VALUE
        и попробуй запустить снова.
        '''))
        sys.exit(1)
with open('./config.yml') as f:
    config = yaml.safe_load(f)
    f.close()





def load_base(q_file):
    """
    Represent function for loading question from file
    args: q_file
    Format of file is:
    question |answer , use | as delimiter

    Фунция загружает базу вопросов для викторины из файла
    Формат файла вопрос|ответ , разделитель символ '|'.
    """
    my_file = open(q_file)
    file_lines = my_file.readlines()
    my_file.close()
    quest_base_ = []
    quest = {}
    #print (l)
    for item in file_lines:
        if len(item.split('|')) >= 2:
            quest['quest'] = item.split('|')[0].strip('\n')
            quest['answ'] = item.split('|')[1].strip('\n')
            quest_base_.append(quest)

        quest = {}
    return quest_base_


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

def bothelp(update, context):
    """
    Send a message when the command /help is issued.
    Посылает сообщение по комаде /help

    """
    chat_id = update.effective_chat.id

    message = HELP_MESSAGE
    context.bot.send_message(chat_id=chat_id, text=message)


def start(update, context):
    """
    Send a message when the command /start is issued.
    Посылает сообщение по комаде /start
    """
    chat_id = update.effective_chat.id

    context.bot.send_message(chat_id=chat_id, text=HELP_MESSAGE)
    print(update.effective_chat.id)




def quiz(update, context):
    """
    Send a message when the command /help is issued.
    Посылает сообщение по комаде /help
    """
    chat_id = update.effective_chat.id
    if state_bot['quest']:
        current_quest = state_bot['q']
        message = _('{} {} ( {} букв)').format(
            current_quest['quest'],
            '*'*len(current_quest['answ']), len(current_quest['answ']))
        context.bot.send_message(chat_id=chat_id, text=message)
    else:
        state_bot['quest'] = True
        current_quest = random.choice(quest_base)
        state_bot['q'] = current_quest
        message = _('{} {} ( {} букв)').format(
            current_quest['quest'], '*'*len(current_quest['answ']), len(current_quest['answ']))
        context.bot.send_message(chat_id=chat_id, text=message)



def mess(update, context):
    """
    Send message for answer on question if state  quest is true,
    counting tries,
    if tries >3 reset game
    check answer with answer in base and if answer is correct say goodboy
    and reset game

    Посылает сообщение на ответ если статус бота quest =true.
    считает попытки ответов,
    сверяет ответ с ответом в базе, если ответ верный то говорит молодец,
    и сбрасывает игру
    если попыток >3 то игра сбрасывается
    """
    chat_id = update.effective_chat.id
    text = update.message.text
    if state_bot['quest']:
        if state_bot['q']['answ'] == text.lower().strip():
            message = _('''Молодец, правильно.
            Набери еще раз /ask для нового вопроса.
            ''')
            state_bot['quest'] = False
            state_bot['q'] = {}
        else:
            message = _('Неверно ')
            state_bot['tries'] = state_bot['tries']+1
            if state_bot['tries'] > 3:
                message = _('''
                    Вопрос: {}
                    не угадали за три попытки
                    Набери еще раз /ask для нового вопроса''').format(
                        state_bot['q']['quest'])
                state_bot['quest'] = False
                state_bot['q'] = {}
                state_bot['tries'] = 0

        context.bot.send_message(chat_id=chat_id, text=message)




TOKEN = config['token']
if LANG == 'ru_RU':
    quest_base = load_base('./quest.txt')
else:
    quest_base = load_base('./quest.{}.txt'.format(LANG))


UPDATER = Updater(token=TOKEN, use_context=True)
DISPATCHER = UPDATER.dispatcher

START_HANDLER = CommandHandler('start', start)
QUIZ_HANDLER = CommandHandler('ask', quiz)
HELP_HANDLER = CommandHandler('help', bothelp)
MESS_HANDLER = MessageHandler(Filters.regex(''), mess)

DISPATCHER.add_handler(START_HANDLER)
DISPATCHER.add_handler(QUIZ_HANDLER)
DISPATCHER.add_handler(HELP_HANDLER)
DISPATCHER.add_handler(MESS_HANDLER)

UPDATER.start_polling()
