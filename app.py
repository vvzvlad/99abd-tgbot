#!/usr/bin/env python3
from peewee import *
import json
import datetime
import telebot
from threading import Thread
import time
import datetime
import random
import operator
import markovify
import schedule
from munch import Munch
import argparse

#coffee camera
from requests.auth import HTTPDigestAuth
import requests
from telebot.types import InputFile

parser = argparse.ArgumentParser()
parser.add_argument('--db', type=str, default="./database/99-abd.db")
args = parser.parse_args()

print("Load markovify models..")
with open('./database/model_combo.json') as file:
  model_json = file.read()
  print("Model combo loaded. Importing..")
  model_combo = markovify.Text.from_json(model_json)
  print("Loaded and imported.")

with open('./database/astra.json') as file:
  model_json = file.read()
  print("Model astra loaded. Importing..")
  model_astra = markovify.Text.from_json(model_json)
  print("Loaded and imported.")

with open('./database/koteeq.json') as file:
  model_json = file.read()
  print("Model koteeq loaded. Importing..")
  model_koteeq = markovify.Text.from_json(model_json)
  print("Loaded and imported.")

db = SqliteDatabase(args.db)

time_delete = 60*10
msg_random = 5

def probability(percent):
  if random.randint(0,100) < percent:
    return True
  return False

def publish_message(reply_to_message, message):
  Thread(target=wait_and_reply,kwargs={'reply_to_message':reply_to_message, 'message':message}).start()
  return True

def is_member(chat_id, user_id):
    try:
        bot.get_chat_member(chat_id, user_id)
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False
    except Exception as e:
            print(f'Unknown error: {e.__class__.__name__}')

def extract_arg(arg):
    return arg.split()[1:]

class Abd(Model):
    username = CharField(column_name='username', null=False)
    user_id = IntegerField(column_name='user_id', primary_key=True)
    join_date = DateTimeField(column_name='join_date')
    last_message_date = DateTimeField(column_name='last_message_date')
    is_admin = BooleanField(column_name='is_admin')
    messages_count = IntegerField(column_name='messages_count')
    group_id = CharField(column_name='group_id')
    class Meta:
        database = db
Abd.create_table()

class Creds(Model):
    creds_name = CharField(primary_key=True)
    creds_value = CharField()
    class Meta:
        database = db
Creds.create_table()
#Creds.create(creds_name='tg_bot_token', creds_value="ХХХ")
#Creds.create(creds_name='tg_bot_id', creds_value="5944502638")
token = Creds.select().where(Creds.creds_name == "tg_bot_token").dicts().execute()[0]["creds_value"]
bot_id = Creds.select().where(Creds.creds_name == "tg_bot_id").dicts().execute()[0]["creds_value"]
bot = telebot.TeleBot(token)


class Query(Model):
    message_id = IntegerField()
    chat_id = IntegerField()
    abs_time_live = DateTimeField()
    class Meta:
        database = db
Query.create_table()










def wait_and_reply(reply_to_message, message):
  time.sleep(random.uniform(1, 4))
  bot.reply_to(reply_to_message, message)

def wait_and_exit_user(chat_id, user_id, username):
  time.sleep(60*10)
  bot.unban_chat_member(chat_id, user_id)
  bot.send_message(chat_id, f"@{username} удален из чата")
  print(f"Kick: username in chat {chat_id}")
  user_for_delete_dbnode = Abd.get(Abd.user_id == user_id)
  user_for_delete_dbnode.delete_instance()

def messages_deleter():
  while True:
    time.sleep(1)
    messages = Query.select().where(Query.abs_time_live < datetime.datetime.today()).dicts().execute()
    for message in messages:
      msg_id = message["message_id"]
      chat_id = message["chat_id"]
      Query.get((Query.message_id == msg_id) & (Query.chat_id == chat_id)).delete_instance()
      try:
        bot.delete_message(chat_id, msg_id)
        print(f"Deleted: {msg_id} in chat {chat_id}")
#      except ApiTelegramException as e:
#        print(f"Not deleted: {msg_id} in chat {chat_id} - {e}")
      except Exception as e:
        print(f'Error: {e.__class__.__name__}')

def schedule_worker():
  chat_id = "-1001387877165" #99
  #chat_id = "-699513317" #test
  message = Munch.fromDict({"chat": {"id": chat_id}, "scheduled": True, "from_user": {"username": "vvzvlad"}})
  schedule.every().day.at("10:32").do(cmd_day_gay, message)
  schedule.every().day.at("13:48").do(cmd_day_faggot, message)
  schedule.every().day.at("16:12").do(cmd_day_furr, message)
  schedule.every().day.at("19:59").do(cmd_day_couple, message)
  schedule.every().day.at("22:02").do(cmd_day_pretty, message)
  schedule.every().day.at("01:02").do(cmd_day_protogen, message)

  schedule.every().monday.at("12:10").do(cmd_99_rotation, message)
  schedule.every().tuesday.at("16:42").do(cmd_99_rotation, message)
  while True:
    time.sleep(1)
    schedule.run_pending()


def queued_message_for_delete(message, time=time_delete):
  if (hasattr(message, "scheduled")) is True: return
  if message.via_bot is not None:
    print(f"Queued: id {message.message_id}: '{message.text}' from {message.from_user.username} via bot {message.via_bot.username} in {time}")
  else:
    print(f"Queued: id {message.message_id}: '{message.text}' from {message.from_user.username} in {time}")
  livetime = datetime.datetime.now() + datetime.timedelta(seconds=time)
  Query.create(message_id=message.message_id, chat_id=message.chat.id, abs_time_live=livetime)

@bot.message_handler(commands=['set_delete_delay'])
def set_delete_delay_cmd(message):
  global time_delete
  admins_table = Abd.select().where(Abd.is_admin == True).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  admins_dict = [d['username'] for d in admins_table]
  if message.from_user.username not in admins_dict:
      msg = bot.reply_to(message, f"Ты не админ")
      queued_message_for_delete(message)
      queued_message_for_delete(msg)
      return
  else:
    time_delete = int(extract_arg(message.text)[0])
    msg = bot.reply_to(message, f"Задержка установлена в {time_delete} секунд")
    queued_message_for_delete(message)
    queued_message_for_delete(msg)


@bot.message_handler(commands=["dg", "dg@ninety_nine_abominable_bot"])
def cmd_day_gay(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+1)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-4)).order_by(Abd.username).dicts().execute()
  user = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"🎉 Сегодня ГЕЙ 🌈 дня (и вечера) (/dg) - @{user}")
  if (hasattr(message, "scheduled")) is False:
    queued_message_for_delete(message)
    queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["df", "df@ninety_nine_abominable_bot"])
def cmd_day_faggot(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+2)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-4)).order_by(Abd.username).dicts().execute()
  user = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"Сегодня ПИДОР 🎉 дня (и вечера) (/df) - @{user}")
  if (hasattr(message, "scheduled")) is False:
    queued_message_for_delete(message)
    queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["dfur", "dfur@ninety_nine_abominable_bot"])
def cmd_day_furr(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+3)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-4)).order_by(Abd.username).dicts().execute()
  user = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"Сегодня 🦄 ФУРРИ 🐶  дня (и вечера) (/dfur) - 🐰 @{user} 🐳")
  if (hasattr(message, "scheduled")) is False:
    queued_message_for_delete(message)
    queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["dc", "dc@ninety_nine_abominable_bot"])
def cmd_day_couple(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+4)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-4)).order_by(Abd.username).dicts().execute()
  p1 = random.choice(users)["username"]
  p2 = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"🎉 Сегодня ПАРА 😳 дня (/dc) - @{p1} и @{p2} 💕 🐕 ЕБИТЕС 🐕")
  if (hasattr(message, "scheduled")) is False:
    queued_message_for_delete(message)
    queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["dp", "dp@ninety_nine_abominable_bot"])
def cmd_day_pretty(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+5)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-4)).order_by(Abd.username).dicts().execute()
  pretty = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"🎉 Сегодня КРАСАВЧИК 😊 дня (/dp) - @{pretty}")
  if (hasattr(message, "scheduled")) is False:
    queued_message_for_delete(message)
    queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["dproto", "dproto@ninety_nine_abominable_bot"])
def cmd_day_protogen(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+6)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-4)).order_by(Abd.username).dicts().execute()
  user = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"🤖 Сегодня ПРОТОГЕН 🤖 дня (и вечера) (/dз) - @{user}")
  if (hasattr(message, "scheduled")) is False:
    queued_message_for_delete(message)
    queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["help", "help@ninety_nine_abominable_bot"])
def cmd_help(message):
  msg = bot.send_message(message.chat.id, f"""🎉 Список команд 🎉
  1. /df - ПЕДИК дня
  1. /dproto - ПРОТОГЕН дня
  5. /dfur - ФУРРИ дня
  5. /dg - ГЕЙ дня
  6. /dc - ПАРА дня
  7. /dp - КРАСАВЧИК дня
  8. /random — сообщение комбинированной модели
  8. /astrandom — сообщение астрологической модели
  8. /koterand — сообщение модели кота
  """)

  queued_message_for_delete(message)
  queued_message_for_delete(msg)

  return


@bot.message_handler(commands=["99_rotation", "99_rotation@ninety_nine_abominable_bot"])
def cmd_99_rotation(message):

  admins_table = Abd.select().where(Abd.is_admin == True).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  admins_dict = [d['username'] for d in admins_table]
  if message.from_user.username not in admins_dict:
    #msg = bot.reply_to(message, f"Нахуй иди")
    msg = bot.send_message(message.chat.id, f"@{message.from_user.username} не боится отправлять команды админов, поэтому его удаление с вероятностью 10% произойдет через час. Приятного дня! Удачной русской рулетки!")
    if (hasattr(message, "scheduled")) is False:
      queued_message_for_delete(message)
      queued_message_for_delete(msg)
    return

  if probability(20):
    msg = bot.reply_to(message, f"Да вы заебали, суууука")
    return

  datetime_3weeks_ago = datetime.datetime.today() + datetime.timedelta(weeks=-3)
  users = Abd.select().where(Abd.last_message_date < datetime_3weeks_ago).order_by(Abd.messages_count, Abd.last_message_date).limit(1).dicts().execute()
  for user in users:
    print(user["last_message_date"], "\t\t", user["messages_count"], "\t", user["username"])
  user_for_delete = users[0]["username"]
  userid_for_delete = users[0]["user_id"]

  bot.send_message(message.chat.id, f"@{user_for_delete} получил это письмо, потому что команда 👨‍🏫 биг дата 👩‍🏫 проанализровала его активности в телеграме и пометила его как невовлеченного 🙈 и малопродуктивного 🙉 шитпостера 🙊. Надя и ее команда заботы  орагнизовали партнерство с ведущими 🤑 шитпост-каналами и мы поможем (нет) найти ему хорошее место, где он будет читать еще больше, а постить еще меньше. Удаление 🚮 произойдет через 10 минут ⏱. Повторная заявка на вступление будет рассмотрена в общем порядке. Еще раз спасибо за вклад (нет). Приятного дня (нет 🤷). С уважением (нет 🤷‍♂️), команда биг дата (нет 🤷‍♀️).")

  Thread(target=wait_and_exit_user,kwargs={'chat_id':message.chat.id, 'user_id':userid_for_delete, 'username':user_for_delete}).start()



@bot.message_handler(commands=["random", "random@ninety_nine_abominable_bot"])
def cmd_random(message):
  queued_message_for_delete(message, time=0.5)
  if message.reply_to_message is not None:
    msg = bot.send_message(message.chat.id, model_combo.make_sentence(), reply_to_message_id=message.reply_to_message.json["message_id"])
    #model_koteeq.make_sentence_with_start(message.reply_to_message.text)
  else:
    msg = bot.reply_to(message, model_combo.make_sentence())
    queued_message_for_delete(msg)

@bot.message_handler(commands=["astrandom", "astra", "astrarandom"])
def cmd_astra_random(message):
  queued_message_for_delete(message, time=0.5)
  if message.reply_to_message is not None:
    msg = bot.send_message(message.chat.id, model_astra.make_sentence(), reply_to_message_id=message.reply_to_message.json["message_id"])
    #model_koteeq.make_sentence_with_start(message.reply_to_message.text)
  else:
    msg = bot.reply_to(message, model_astra.make_sentence())
    queued_message_for_delete(msg)

@bot.message_handler(commands=["koterand",  "koterandom", "koteeq" "koteeqrandom"])
def cmd_koteeq_random(message):
  queued_message_for_delete(message, time=0.5)
  if message.reply_to_message is not None:
    msg = bot.send_message(message.chat.id, model_koteeq.make_sentence(), reply_to_message_id=message.reply_to_message.json["message_id"])
    #model_koteeq.make_sentence_with_start(message.reply_to_message.text)
  else:
    msg = bot.reply_to(message, model_koteeq.make_sentence())
    queued_message_for_delete(msg)

def counter_update(message):
  first_name = message.from_user.first_name or ""
  last_name = message.from_user.last_name or ""
  if last_name != "":
    last_name = " " + last_name
  username = message.from_user.username or (first_name + last_name)

  try:
    user = Abd.get(Abd.user_id == message.from_user.id)
    Abd.update(messages_count=user.messages_count + 1, last_message_date=datetime.datetime.today()).where(Abd.user_id == message.from_user.id).execute()
  except Abd.DoesNotExist:
    Abd.create(username=username, user_id=message.from_user.id, join_date=datetime.datetime.today(), last_message_date=datetime.datetime.today(), is_admin=False, messages_count=1, group_id=message.chat.id)

def random_message(message):
  if message.text[0] != "/" and probability(msg_random):
    #rnd_count = random.randrange(0, 100, 1)
    #if rnd_count < 50:
    #  gen_message = model_combo.make_sentence()
    #if rnd_count >= 50 and rnd_count < 75:
    #  gen_message = 'Астра на это бы сказала "' + model_astra.make_sentence() + '"'
    #if rnd_count >= 75:
    #  gen_message = 'Аня на это бы сказала "' + model_koteeq.make_sentence() + '"'

    gen_message = model_astra.make_sentence()

    publish_message(message, gen_message)

def random_cunt_message(message):
  message_text = message.text.lower()
  if message.reply_to_message is not None:
    if int(message.reply_to_message.json["from"]["id"]) == int(bot_id):
      if (message_text == "хуй в уста") and probability(100):
        return publish_message(message, "астры ответ")
      if (message_text == "бота аргумент") and probability(100):
        return publish_message(message, "аргумент не нужен, бот не обнаружен")
      return True

  if message_text.find("астра") >= 0 and probability(5):
    return publish_message(message, "хуястра!")
  if message_text.find("астры") >= 0 and probability(10):
    return publish_message(message, "хуястры!")
  if message_text.find("астру") >= 0 and probability(10):
    return publish_message(message, "хуястру!")
  if message_text.find("астрой") >= 0 and probability(10):
    return publish_message(message, "хуястрой!")

  if message_text.find("пидора ответ") >= 0 and probability(50):
    return publish_message(message, "шлюхи аргумент")

  if (message_text.find("uwu") >= 0 or message_text.find("уву") >= 0) and probability(20):
    return publish_message(message, "Подавился?")
  if message_text.find("где?") >= 0 and probability(20):
    return publish_message(message, "В пизде")

  if (message_text == "да") and probability(10):
    return publish_message(message, "пизда")
  if (message_text == "пизда") and probability(10):
    return publish_message(message, "хуй в уста")
  if (message_text == "нет") and probability(10):
    return publish_message(message, "пидора ответ")

  return False

def delete_bots_messages(message):
  if message.via_bot is not None:
    delete_bots = ["yepcock_size_bot", "PredskazBot", "HowAllBot", "FairCocksizeBot", "ManPercentBot", "rus_cocksize_bot", "HowYourBot", "penis_size_checker_bot"]
    if message.via_bot.username in delete_bots:
      queued_message_for_delete(message)
      return True
  return False


def find_reply_to_queued(message):
  if message.reply_to_message is not None:
    reply_to_user_id = int(message.reply_to_message.json["from"]["id"])
    reply_to_message_id = int(message.reply_to_message.json["message_id"])
    reply_in_chat_id = int(message.reply_to_message.chat.id)
    if reply_to_user_id == int(bot_id):
      try:
        Query.get((Query.message_id == reply_to_message_id) & (Query.chat_id == reply_in_chat_id)).delete_instance()
        print(f"Unqueued: {reply_to_message_id} in {reply_in_chat_id}")
      except Query.DoesNotExist:
        pass

@bot.message_handler()
def all_messages(message):
  print(message)

  if delete_bots_messages(message): return
  find_reply_to_queued(message)
  counter_update(message)
  if random_cunt_message(message): return
  random_message(message)


Thread(target=messages_deleter).start()
Thread(target=schedule_worker).start()
print("Bot started")
bot.infinity_polling()









