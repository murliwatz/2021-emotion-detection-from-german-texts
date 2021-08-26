import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

words_file = open(sys.argv[1], encoding="utf8")

for w in words_file.readlines():
    sys.stdout.buffer.write(ps.stem(w).encode('utf8'))
