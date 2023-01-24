#!/usr/bin/env python3
import json
import os

directory = "./datasets/raw_tg_chats"



def parse_default():
  for (dirpath, _, filenames) in os.walk(directory):
      for filename in filenames:
        with open(directory+"/"+filename) as json_file:
          count = 0
          print("Parsing file: "+filename)
          try:
            fp = open(directory+filename+".txt", 'w')
            messages = json.load(json_file)["messages"]
            for message in messages:
              count += 1
              if message['type'] == 'message':
                if 'via_bot' not in message:
                  if isinstance(message['text'], str):
                      if len(message['text']) > 3:
                        message['text'] = message['text'].replace("\r", ". ").replace("\n", ". ")
                        #print(count, message['text'], flush=True)
                        fp.write(message['text'] + "\n")
            fp.close()
          except Exception as e:
            print("Error parsing file: "+filename)
            print(e)
          print("Done parsing file: "+filename + "count: "+str(count))


def parse_user(user_id, username):
  fp = open(username+".txt", 'w')
  for (dirpath, _, filenames) in os.walk(directory):
      for filename in filenames:
        with open(directory+"/"+filename) as json_file:
          count = 0
          print("Parsing file: "+filename)
          try:
            messages = json.load(json_file)["messages"]
            for message in messages:
              if message['type'] == 'message':
                if 'via_bot' not in message:
                  if isinstance(message['text'], str):
                    if message['from_id'] == "user"+user_id:
                      if len(message['text']) > 3:
                        message['text'] = message['text'].replace("\r", ". ").replace("\n", ". ")
                        count += 1
                        #print(count, message['text'], flush=True)
                        #print(message)
                        fp.write(message['text'] + "\n")
          except Exception as e:
            print("Error parsing file: "+filename)
            print(e)
          print("Done parsing file: "+filename + ", "+username+"'s messages: "+str(count))
  fp.close()







#parse_default()

#parse_user("1809232593", "astra")
#parse_user("944809", "koteeq")
#parse_user("545921945", "rozetkin")
#parse_user("5862421303", "ledrod")
#parse_user("37796149", "spherebread")
parse_user("421481894", "N30F0X")




