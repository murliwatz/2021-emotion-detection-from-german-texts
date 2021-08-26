import spacy
import sys
nlp = spacy.load('de_core_news_lg')

mails=open(sys.argv[1], encoding="utf8").read().splitlines()
stopwords=open('data/stopwords/german_stopwords_full.txt', encoding="utf8").read().splitlines()

counts = dict()

mails_lemma = []

for mail in mails:
    doc = nlp(mail.lower())
    for x in doc:
        if x.lemma_ not in stopwords:
            if x.lemma_ in counts:
                counts[x.lemma_] += 1
            else:
                counts[x.lemma_] = 1

s = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
for i in s:
    if s[i] > 10 and len(i) > 3:
        print(i, s[i])
