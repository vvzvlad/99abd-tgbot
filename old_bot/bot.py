#!/usr/bin/env python3

import telebot
from threading import Thread
import time
import datetime
import random
from tinydb import TinyDB, Query
import operator


db = TinyDB('./db.json')
token="5944502638:AAEh4jB3t0wPA8KFJX8giewdTkGN7HcJcw8"
messages = ["Бля, а доказать сможешь?", "Обоснуй", "Ой, кажется мне, ты пиздишь", "Нихуя себе", "Ты чо, ебнулся?", "Ты чо, ебанулся?", "В жопу себе это засунь", "Не обижайся, но ты долбоеб", "Мой герой!", "Тебе заняться нечем?", "Сексизм какой-то", "А в чем суть?", "Расскажи нормально, не понял нихуя", "О, это прекрасно"]
delete_bots = ["yepcock_size_bot", "PredskazBot", "HowAllBot", "FairCocksizeBot", "ManPercentBot", "rus_cocksize_bot", "HowYourBot"]
admins = ["vvzvlad", "astrra", "Dr_Zlo13", "koteeq"]
User = Query()
bot=telebot.TeleBot(token)
time_delete = 60*10




@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет")





@bot.message_handler(commands=['set_delete_delay'])
def set_delete_delay_cmd(message):
  if message.from_user.username not in admins:
      msg = bot.reply_to(message, f"Ты не админ")
      Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':time_delete}).start()
      Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':time_delete}).start()
      return
  else:
    time_delete = int(extract_arg(message.text)[0])
    msg = bot.reply_to(message, f"Задержка установлена в {time_delete} секунд")
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':time_delete}).start()
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':time_delete}).start()


@bot.message_handler(commands=['bruh', "gay", "ass", "bi", "booba", "cock", "sex", "protogen", "straight", "rozetkin"])
def bruh_cmd(message):
  msg = bot.reply_to(message, f"чел смыл хомяка!")
  Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':60}).start()
  Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':60}).start()


@bot.message_handler(commands=["koteeq", "astra", "astrra"])
def bruh_cmd(message):
  msg = bot.reply_to(message, f"она норм")
  Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':60}).start()
  Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':60}).start()





@bot.message_handler()
def answers(message):
#  print(message)

  current_username = message.from_user.username


  #db.upsert({'name': 'John', 'logged-in': True}, User.name == 'John')
  db_search = db.search(User.name == current_username)
  if len(db_search) == 0:
    db.insert({'name': current_username, 'count': 1, 'last_message': int(time.time())})
  else:
    current_user_count = db_search[0]['count']
    db.update({'count': current_user_count + 1, 'last_message': int(time.time())}, User.name == current_username)



  if message.text == "/dg" or message.text == "/dg@ninety_nine_abominable_bot":
    date_string = datetime.datetime.today().strftime('%d/%m/%Y')
    epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
    random.seed(epoch_date+1)
    db_search = db.search(User.count > 1)
    day_gay = random.choice(db_search)["name"]
    msg = bot.send_message(message.chat.id, f"🎉 Сегодня ГЕЙ 🌈 дня (и вечера) (/dg) - @{day_gay}")
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':3}).start()
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':time_delete}).start()
    random.seed()
    return

  if message.text == "/df" or message.text == "/df@ninety_nine_abominable_bot":
    date_string = datetime.datetime.today().strftime('%d/%m/%Y')
    epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
    random.seed(epoch_date+4)
    db_search = db.search(User.count > 1)
    day_farrot = random.choice(db_search)["name"]
    msg = bot.send_message(message.chat.id, f"Сегодня ПИДОР 🎉 дня (и вечера) (/df) - @{day_farrot}")
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':3}).start()
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':time_delete}).start()
    random.seed()
    return

  if message.text == "/dc" or message.text == "/dc@ninety_nine_abominable_bot" :
    date_string = datetime.datetime.today().strftime('%d/%m/%Y')
    epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
    random.seed(epoch_date+2)
    db_search = db.search(User.count > 1)
    p1 = random.choice(db_search)["name"]
    p2 = random.choice(db_search)["name"]
    msg = bot.send_message(message.chat.id, f"🎉 Сегодня ПАРА 😳 дня (/dc) - @{p1} и @{p2} 💕 ")
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':3}).start()
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':time_delete}).start()
    random.seed()
    return

  if message.text == "/dp" or message.text == "/dp@ninety_nine_abominable_bot":
    date_string = datetime.datetime.today().strftime('%d/%m/%Y')
    epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
    random.seed(epoch_date+3)
    db_search = db.search(User.count > 1)
    pretty = random.choice(db_search)["name"]
    msg = bot.send_message(message.chat.id, f"🎉 Сегодня КРАСАВЧИК 😊 дня (/dp) - @{pretty}")
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':3}).start()
    Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':time_delete}).start()
    random.seed()
    return

  if message.text == "/clean":
    if message.from_user.username not in admins:
      msg = bot.reply_to(message, f"Ты не админ")
      Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':time_delete}).start()
      Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':msg.message_id, 'wait_time':time_delete}).start()
      return

    db_search = db.all()
    db_search.sort(key=lambda item:item['last_message'], reverse=False)
    for user in db_search:
      if is_member(message.chat.id, user["name"]):
        msg = bot.reply_to(message, f"Будет удален пользователь @{user['name']}")
      else:
        db.remove(User.name == user["name"])
      print(user["name"], user["last_message"], user["count"])


    #msg = bot.send_message(message.chat.id, f"{db_search}")
    return

  if message.via_bot is not None:
    if message.via_bot.username in delete_bots:
      Thread(target=wait_and_delete,kwargs={'chat_id':message.chat.id, 'message_id':message.message_id, 'wait_time':60*10}).start()
      print(f"Queued: {message.text} from {message.from_user.username} via bot {message.via_bot.username}")
      return

  if random.randrange(0, 200, 1) == 0:
    Thread(target=wait_and_reply,kwargs={'message':message}).start()













  #print(f"{message.text} {message.chat.type} {message.chat.id}")


bot.infinity_polling()



