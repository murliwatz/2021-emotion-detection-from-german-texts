import spacy
import sys
import os
import yaml
import copy
import re

nlp = spacy.load('de_core_news_lg')

tokens = set()

lines = open(sys.argv[1], encoding="utf8").read().splitlines()
for line in lines:
    if len(line.split(' ')) == 1:
        tokens.add(line)
        tokens.add(nlp(line)[0].lemma_)

sys.stdout.buffer.write('\n'.join(tokens).encode('utf8'))
