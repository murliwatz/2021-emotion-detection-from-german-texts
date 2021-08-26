import spacy
import sys
nlp = spacy.load('de_core_news_lg')

mails=open(sys.argv[1], encoding="utf8").read().splitlines()

mails_lemma = []

for mail in mails:
     doc = nlp(mail)
     result = ' '.join([x.lemma_ for x in doc])
     mails_lemma.append(result)

print(mails_lemma)
