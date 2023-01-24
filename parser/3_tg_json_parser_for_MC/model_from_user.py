#!/usr/bin/env python3
import json
import os
import markovify


user = "astra"

print("Load "+user+" corpus..")
with open("./"+user+".txt") as f:
  forced = f.read()
  print("Loaded, generate model..")
markovify_model = markovify.NewlineText(forced, state_size=2, retain_original=False)
print("Generated.")



print("Export model..")
model_json = markovify_model.to_json()
with open(user+'.json', 'w') as outfile:
    outfile.write(model_json)



print("Test load markovify model..")
with open(user+'.json') as file:
  import_model_json = file.read()
  print("Loaded. Importing..")
  reconstituted_model = markovify.Text.from_json(import_model_json)
print("Loaded and imported.")

print(reconstituted_model.make_short_sentence(280))









