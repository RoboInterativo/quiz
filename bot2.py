
from telegram.ext import Updater
from telegram.ext import CommandHandler,MessageHandler,Filters
import logging
import yaml
import json
import random
import os
import sys

#import docker
state_bot={'tries':0,'quest': False,'q':{}  }

#os.environ.get('TOKEN')

with open('./config.yml','w') as f:

    if os.environ.get('TOKEN') !=None:
        config={'token': os.environ.get('TOKEN')}
        f.write( yaml.dump (config) )
        f.close()
    else:
        print ('''
        TOKEN not set
        set env by type
        export TOKEN=TOKEN_VALUE
        and try again.
        -----------------------
        Не установлена переменная TOKEN
        для ее установки Набери
        export TOKEN=TOKEN_VALUE
        и попробуй запустить снова.
        ''' )
        sys.exit(1)
with open('./config.yml') as f:
    config = yaml.safe_load(f)
    f.close()





def load_base(q_file):
    f=open(q_file)
    l=f.readlines()
    f.close()
    qb=[]
    q={}
    #print (l)
    for el in l:
        if len (el.split('|') )>=2:
            q['quest']=el.split('|')[0].strip('\n')
            q['answ']=el.split('|')[1].strip('\n')
            qb.append(q)

        q={}
    return qb
#print (tok)
default_message_for_not_members="""
Привет это викторина , для запуска набери /ask
"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG)


def start(update, context):
    chat_id=update.effective_chat.id
    #-462030398,

    #if chat_id==-466179676:
    #
    context.bot.send_message(
        chat_id=chat_id, text="Запусти викторину /ask" )
    print(update.effective_chat.id)
   # else:
   #    context.bot.send_message(   chat_id=chat_id,
   #    text=default_message_for_not_members)
   #    print(update.effective_chat.id)

def quiz(update, context):
    chat_id=update.effective_chat.id
    if state_bot['quest']:
            tr= state_bot['q']
            message='{} {} ( {} букв)'.format(tr['quest'],  '*' * len(tr['answ']),  len(tr['answ'])  )
            context.bot.send_message(        chat_id=chat_id, text=message )
    else:
        state_bot['quest']=True
        tr=random.choice(qb)
        state_bot['q']=tr
        message='{} {} ( {} букв)'.format(tr['quest'],  '*' * len(tr['answ']),  len(tr['answ'])  )
        context.bot.send_message(        chat_id=chat_id, text=message )



def mess(update, context):
    chat_id=update.effective_chat.id
    text=update.message.text
    if state_bot['quest']:
        if state_bot['q']['answ']==text.lower().strip():
        #m='{}-{}'.format (text, state_bot['q']['answ'])
            m='''Молодец, правильно.
              Набери еще раз /ask для нового вопроса.
            '''
            state_bot['quest']=False
            state_bot['q']={}
        else:
            m='Неверно '
            state_bot['tries']=state_bot['tries']+1

            if state_bot['tries']>3:
               m='''Вопрос: {}
                   не угадали за три попытки
                   Набери еще раз /ask для нового вопроса'''.format (state_bot['q']['quest'] )
               state_bot['quest']=False
               state_bot['q']={}
               state_bot['tries']=0
#.format (state_bot['q']['answ']  )
        context.bot.send_message(        chat_id=chat_id, text= m )






TOKEN=config ['token']
qb=load_base('./quest.txt')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
quiz_handler = CommandHandler('ask', quiz)
mess_hanlder =MessageHandler(Filters.regex(''),mess)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(quiz_handler)
dispatcher.add_handler(mess_hanlder)

updater.start_polling()
