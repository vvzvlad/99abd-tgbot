#!/usr/bin/env python3
import asyncio
from pyrogram import Client
import json

api_id = 0
api_hash = "-"
chat_id = -1001387877165


async def main():
  members = []
  async with Client("my_account", api_id, api_hash) as app:
    async for member in app.get_chat_members(chat_id):
      first_name = member.user.first_name or ""
      last_name = member.user.last_name or ""
      if last_name != "":
        last_name = " " + last_name
      username = member.user.username or first_name + last_name
      members.append({"join_date": str(member.joined_date), "user_id": str(member.user.id), "username": username, "admin": str(member.status)})

  print(json.dumps(members, ensure_ascii=False))

#async def main():
#  members = []
#  async with Client("my_account", api_id, api_hash) as app:
#    async for member in app.get_chat_members(chat_id):
#      print(member)


#async def main():
#  members = []
#  async with Client("my_account", api_id, api_hash) as app:
#    async for member in app.get_chat_members(chat_id):
#      if member.user.id == 540668259:
#        print(member)
#        first_name = member.user.first_name or ""
#        last_name = member.user.last_name or ""
#        if last_name != "":
#          last_name = " " + last_name
#        username = member.user.username or first_name + last_name
#        print(json.dumps({"join_date": str(member.joined_date), "user_id": str(member.user.id), "username": username, "admin": str(member.status)}, ensure_ascii=False))



asyncio.run(main())
