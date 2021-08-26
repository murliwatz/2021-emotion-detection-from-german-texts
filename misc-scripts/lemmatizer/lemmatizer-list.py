import spacy
import sys
nlp = spacy.load('de_core_news_lg')

mails=open(sys.argv[1], encoding="utf8").read().splitlines()

s = set()

for mail in mails:
     doc = nlp(mail)
     s.add(mail)
     s.add(doc[0].lemma_)

for s_ in s:
    print(s_)
