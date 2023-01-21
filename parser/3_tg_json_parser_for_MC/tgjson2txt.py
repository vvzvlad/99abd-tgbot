#!/usr/bin/env python3
import json
import os

directory = "./datasets/"





for (dirpath, _, filenames) in os.walk(directory):
    for filename in filenames:
      with open(directory+filename) as json_file:
        print("Parsing file: "+filename)
        try:
          fp = open(directory+filename+".txt", 'w')
          messages = json.load(json_file)["messages"]
          count = 0
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





















