#!/usr/bin/env python3
import json
import datetime
import markovify

with open("./99_corpus.txt") as f:
    text = f.read()


text_model = markovify.NewlineText(text, state_size=2)

for i in range(5):
    print(text_model.make_sentence())

for i in range(3):
    print(text_model.make_short_sentence(280))


















