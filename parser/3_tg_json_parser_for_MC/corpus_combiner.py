#!/usr/bin/env python3
import json
import os
import markovify


print("Load ru_arduino corpus..")
with open("./datasets/txt/ru_arduino.json.txt") as f:
  ru_arduino = f.read()
print("Loaded, generate model..")
markovify_ru_arduino_model = markovify.NewlineText(ru_arduino, state_size=2, retain_original=False)
print("Generated.")

print("Load flipper_main corpus..")
with open("./datasets/txt/main_export_chat.json.txt") as f:
  flipper_main_chat = f.read()
  print("Loaded, generate model..")
markovify_flipper_main_chat_model = markovify.NewlineText(flipper_main_chat, state_size=2, retain_original=False)
print("Generated.")

print("Load electronics corpus..")
with open("./datasets/txt/electronics.json.txt") as f:
  electronics = f.read()
  print("Loaded, generate model..")
markovify_electronics_model = markovify.NewlineText(electronics, state_size=2, retain_original=False)
print("Generated.")

print("Load flipper_99 corpus..")
with open("./datasets/txt/99_export_chat.json.txt") as f:
  flipper_99_chat = f.read()
  print("Loaded, generate model..")
markovify_flipper_99_chat_model = markovify.NewlineText(flipper_99_chat, state_size=2, retain_original=False)
print("Generated.")

print("Load antivacs corpus..")
with open("./datasets/txt/ProtivGadov5.json.txt") as f:
  antivacs = f.read()
  print("Loaded, generate model..")
markovify_antivacs_model = markovify.NewlineText(antivacs, state_size=2, retain_original=False)
print("Generated.")

print("Load zhovner corpus..")
with open("./datasets/txt/zhovner.json.txt") as f:
  zhovner = f.read()
  print("Loaded, generate model..")
markovify_zhovner_model = markovify.NewlineText(zhovner, state_size=2, retain_original=False)
print("Generated.")

print("Load flipper_offtopic corpus..")
with open("./datasets/txt/offtopic_export_chat.json.txt") as f:
  flipper_offtopic_chat = f.read()
  print("Loaded, generate model..")
markovify_flipper_offtopic_chat_model = markovify.NewlineText(flipper_offtopic_chat, state_size=2, retain_original=False)
print("Generated.")

print("Load forcedme corpus..")
with open("./datasets/txt/forced.json.txt") as f:
  forced = f.read()
  print("Loaded, generate model..")
markovify_forced_model = markovify.NewlineText(forced, state_size=2, retain_original=False)
print("Generated.")


print("Combine models..")
model_combo = markovify.combine([ markovify_flipper_99_chat_model,
                                  markovify_flipper_offtopic_chat_model,
                                  markovify_flipper_main_chat_model,
                                  markovify_forced_model,
                                  markovify_zhovner_model,
                                  markovify_electronics_model,
                                  markovify_ru_arduino_model,
                                  markovify_antivacs_model ],
                                  [ 1.5,
                                    0.3,
                                    0.3,
                                    1.2,
                                    1.2,
                                    0.1,
                                    0.1,
                                    0.3 ])
print("Combined.")


print("Export model..")
model_json = model_combo.to_json()
with open('model_combo.json', 'w') as outfile:
    outfile.write(model_json)



print("Test load markovify model..")
with open('model_combo.json') as file:
  import_model_json = file.read()
  print("Loaded. Importing..")
  reconstituted_model = markovify.Text.from_json(import_model_json)
print("Loaded and imported.")

print(reconstituted_model.make_short_sentence(280))









