#!/usr/bin/env python3
from peewee import *
import json
import datetime

db = SqliteDatabase('99-abd.db')


#  {
#    "join_date": "2022-05-26 19:38:01",
#    "user_id": "85106994",
#    "username": "vvzvlad",
#    "admin": "ChatMemberStatus.ADMINISTRATOR"
#  },
#{'join_date': '2022-07-24 17:24:15', 'user_id': '383043181', 'username': 'vyacheslavkazakov', 'admin': 'ChatMemberStatus.MEMBER'}




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


with open('members.json') as json_file:
    members = json.load(json_file)
    for member in members:
      if member['admin'] == 'ChatMemberStatus.ADMINISTRATOR':
        member['admin'] = True
      else:
        member['admin'] = False

      #if str(member['join_date']) != "None":
      #  member['join_date'] = datetime.datetime.strptime(member['join_date'], "%Y-%m-%dT%H:%M:%S")

      print(member)
      Abd.create(username=member['username'], user_id=member['user_id'], join_date=member['join_date'], last_message_date=member['join_date'], is_admin=member['admin'], messages_count=0, group_id="-1001387877165")

#  {
#   "id": 1,
#   "type": "service",
#   "date": "2022-05-26T00:43:22",
#   "date_unixtime": "1653515002",
#   "actor": "[NSFW] [NSFL] 99 Flippers [NSFA]",
#   "actor_id": "channel1387877165",
#   "action": "migrate_from_group",
#   "title": "Abominable flippers",
#   "text": "",
#   "text_entities": []
#  },
#  {
#   "id": 3,
#   "type": "message",
#   "date": "2022-05-26T00:44:15",
#   "date_unixtime": "1653515055",
#   "from": "N30F0X",
#   "from_id": "user421481894",
#   "file": "(File not included. Change data exporting settings to download.)",
#   "thumbnail": "(File not included. Change data exporting settings to download.)",
#   "media_type": "sticker",
#   "sticker_emoji": "😏",
#   "width": 512,
#   "height": 403,
#   "text": "",
#   "text_entities": []
#  },
#  {





with open('99_export_chat.json') as json_file:
    messages = json.load(json_file)["messages"]
    count = 0
    for message in messages:
      count += 1
      print(count)
      if message['type'] == 'message':
        message['from_id'] = message['from_id'].replace('user', '')
        try:
          user = Abd.get(Abd.user_id == message['from_id'])
          Abd.update(messages_count=user.messages_count + 1, last_message_date=message['date']).where(Abd.user_id == message['from_id']).execute()
        except Abd.DoesNotExist:
          pass
















