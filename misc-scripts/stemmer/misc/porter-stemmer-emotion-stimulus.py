# http://www.site.uottawa.ca/~diana/resources/emotion_stimulus_data/

import sys
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

ps = PorterStemmer()

stopwords = open("stopwords-en.txt", encoding="utf8").read().splitlines()

words_file = open(sys.argv[1], encoding="utf8")

for line in words_file.read().splitlines():
    if "<happy>" in line:
        words = word_tokenize(line.lower().lstrip("<happy>").rstrip("<\happy>"))
        for w in words:
            if w not in stopwords:
                sys.stdout.buffer.write((ps.stem(w) + "\n").encode('utf8'))
