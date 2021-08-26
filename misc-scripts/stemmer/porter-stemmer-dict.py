import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

words_file = open(sys.argv[1], encoding="utf8")

for w in words_file.readlines():
    w1 = w.split("\t")[0]
    w2 = w.split("\t")[1].lower().rstrip("\n")
    sys.stdout.buffer.write((w1 + "\t" + ps.stem(w2) + "\n").encode('utf8'))
