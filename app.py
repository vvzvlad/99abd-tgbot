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

with open("./database/99_corpus.txt") as f:
    text = f.read()
markovify_text_model = markovify.NewlineText(text, state_size=2)

db = SqliteDatabase('./database/99-abd.db')

time_delete = 60*10
msg_random = 100

def is_member(chat_id, user_id):
    try:
        bot.get_chat_member(chat_id, user_id)
        return True
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False

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
  time.sleep(random.uniform(2, 8))
  bot.reply_to(reply_to_message, message)

def wait_and_exit_user(chat_id, user_id, username):
  time.sleep(10)
  bot.unban_chat_member(chat_id, user_id)
  bot.send_message(chat_id, f"@{username} удален из чата")
  print(f"Kick: username in chat {chat_id}")

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
      except telebot.apihelper.ApiTelegramException as e:
        print(f"Not deleted: {msg_id} in chat {chat_id} - {e}")




def queued_message_for_delete(message):
  if message.via_bot is not None:
    print(f"Queued: id {message.message_id}: '{message.text}' from {message.from_user.username} via bot {message.via_bot.username} in {time_delete}")
  else:
    print(f"Queued: id {message.message_id}: '{message.text}' from {message.from_user.username} in {time_delete}")
  livetime = datetime.datetime.now() + datetime.timedelta(seconds=time_delete)
  Query.create(message_id=message.message_id, chat_id=message.chat.id, abs_time_live=livetime)

@bot.message_handler(commands=["dg", "dg@ninety_nine_abominable_bot"])
def cmd_day_gay(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+1)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-3)).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  day_gay = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"🎉 Сегодня ГЕЙ 🌈 дня (и вечера) (/dg) - @{day_gay}")
  queued_message_for_delete(message)
  queued_message_for_delete(msg)
  random.seed()
  return

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

@bot.message_handler(commands=['set_random'])
def set_ramdom_cmd(message):
  global msg_random
  admins_table = Abd.select().where(Abd.is_admin == True).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  admins_dict = [d['username'] for d in admins_table]
  if message.from_user.username not in admins_dict:
      msg = bot.reply_to(message, f"Ты не админ")
      queued_message_for_delete(message)
      queued_message_for_delete(msg)
      return
  else:
    msg_random = int(extract_arg(message.text)[0])
    msg = bot.reply_to(message, f"Рандомные сообщений будут показываться каждый {msg_random} сообщений")
    queued_message_for_delete(message)
    queued_message_for_delete(msg)

@bot.message_handler(commands=["df", "df@ninety_nine_abominable_bot"])
def cmd_day_faggot(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+4)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-3)).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  day_farrot = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"Сегодня ПИДОР 🎉 дня (и вечера) (/df) - @{day_farrot}")
  queued_message_for_delete(message)
  queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["dc", "dc@ninety_nine_abominable_bot"])
def cmd_day_couple(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+2)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-3)).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  p1 = random.choice(users)["username"]
  p2 = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"🎉 Сегодня ПАРА 😳 дня (/dc) - @{p1} и @{p2} 💕 🐕 ЕБИТЕС 🐕")
  queued_message_for_delete(message)
  queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["dp", "dp@ninety_nine_abominable_bot"])
def cmd_day_pretty(message):
  date_string = datetime.datetime.today().strftime('%d/%m/%Y')
  epoch_date = int(time.mktime(datetime.datetime.strptime(date_string, "%d/%m/%Y").timetuple()))
  random.seed(epoch_date+3)
  users = Abd.select().where(Abd.last_message_date > datetime.datetime.today() + datetime.timedelta(weeks=-3)).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  pretty = random.choice(users)["username"]
  msg = bot.send_message(message.chat.id, f"🎉 Сегодня КРАСАВЧИК 😊 дня (/dp) - @{pretty}")
  queued_message_for_delete(message)
  queued_message_for_delete(msg)
  random.seed()
  return

@bot.message_handler(commands=["99_rotation", "99_rotation@ninety_nine_abominable_bot"])
def cmd_99_rotation(message):
  admins_table = Abd.select().where(Abd.is_admin == True).order_by(Abd.messages_count, Abd.last_message_date).dicts().execute()
  admins_dict = [d['username'] for d in admins_table]
  if message.from_user.username not in admins_dict:
    msg = bot.reply_to(message, f"Ты не админ")
    queued_message_for_delete(message)
    queued_message_for_delete(msg)
    return

  datetime_3weeks_ago = datetime.datetime.today() + datetime.timedelta(weeks=-3)
  users = Abd.select().where(Abd.last_message_date < datetime_3weeks_ago).order_by(Abd.messages_count, Abd.last_message_date).limit(1).dicts().execute()
  for user in users:
    print(user["last_message_date"], "\t\t", user["messages_count"], "\t", user["username"])
  user_for_delete = users[0]["username"]
  userid_for_delete = users[0]["user_id"]

  bot.send_message(message.chat.id, f"@{user_for_delete} получил это письмо, потому что команда 👨‍🏫 биг дата 👩‍🏫 проанализровала его активности в телеграме и пометила его как невовлеченного 🙈 и малопродуктивного 🙉 шитпостера 🙊. Надя и ее команда заботы  орагнизовали партнерство с ведущими 🤑 шитпост-каналами и мы поможем (нет) найти ему хорошее место, где он будет читать еще больше, а постить еще меньше. Удаление 🚮 произойдет через 10 секунд ⏱. Повторная заявка на вступление будет рассмотрена в общем порядке. Еще раз спасибо за вклад (нет). Приятного дня (нет 🤷). С уважением (нет 🤷‍♂️), команда биг дата (нет 🤷‍♀️).")

  Thread(target=wait_and_exit_user,kwargs={'chat_id':message.chat.id, 'user_id':userid_for_delete, 'username':user_for_delete}).start()

  user_for_delete_dbnode = Abd.get(Abd.user_id == userid_for_delete)
  user_for_delete_dbnode.delete_instance()

@bot.message_handler(commands=["random", "random@ninety_nine_abominable_bot"])
def cmd_random(message):
  Thread(target=wait_and_reply,kwargs={'reply_to_message':message, 'message':markovify_text_model.make_sentence()}).start()

def counter_update(message):
  current_username = message.from_user.username
  try:
    user = Abd.get(Abd.user_id == message.from_user.id)
    Abd.update(messages_count=user.messages_count + 1, last_message_date=datetime.datetime.today()).where(Abd.user_id == message.from_user.id).execute()
  except Abd.DoesNotExist:
    Abd.create(username=message.from_user.username, user_id=message.from_user.id, join_date=datetime.datetime.today(), last_message_date=datetime.datetime.today(), is_admin=False, messages_count=1, group_id=message.chat.id)

def random_message(message):
  rnd_count = random.randrange(0, msg_random, 1)
  if message.text[0] != "/" and rnd_count == 0:
    #messages = ["Бля, а доказать сможешь?", "Обоснуй", "Ой, кажется мне, ты пиздишь", "Нихуя себе", "Ты чо, ебнулся?", "Ты чо, ебанулся?", "В жопу себе это засунь", "Не обижайся, но ты долбоеб", "Мой герой!", "Тебе заняться нечем?", "Сексизм какой-то", "А в чем суть?", "Расскажи нормально, не понял нихуя", "О, это прекрасно"]
    Thread(target=wait_and_reply,kwargs={'reply_to_message':message, 'message':markovify_text_model.make_sentence()}).start()

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
    print(reply_to_user_id)
    if reply_to_user_id == int(bot_id):
      print(reply_to_user_id, reply_to_message_id, reply_in_chat_id)
      try:
        Query.get((Query.message_id == reply_to_message_id) & (Query.chat_id == reply_in_chat_id)).delete_instance()
        print(f"Unqueued: {reply_to_message_id} in {reply_in_chat_id}")
      except Query.DoesNotExist:
        pass

@bot.message_handler()
def all_messages(message):
  #print(message)

  if delete_bots_messages(message): return
  find_reply_to_queued(message)
  counter_update(message)
  random_message(message)


Thread(target=messages_deleter).start()
bot.infinity_polling()









