import spacy
import sys
nlp = spacy.load('de_core_news_lg')

mails=open(sys.argv[1], encoding="utf8").read().splitlines()
stopwords=open('data/stopwords/german_stopwords_full.txt', encoding="utf8").read().splitlines()

stopwords.append('offense')
stopwords.append('insult')
stopwords.append('abuse')
stopwords.append('|lbr|')
stopwords.append('....')

sets = list()

mails_lemma = []

for mail in mails:
    doc = nlp(mail.lower())
    s = set()
    f = False
    f2 = False
    for x in doc:
        if x.lemma_ not in stopwords and len(x.lemma_) > 3:
            s.add(x.lemma_)
            if x.lemma_ == 'deutsch':
                f = True
            if x.lemma_ == 'merkel':
                f2 = True
    if f and f2:
        print(mail)
    sets.append(s)

d = dict()

seen = set()

i = 0
for s in sets:
    i += 1
    j = 0
    for s2 in sets:
        j += 1
        if j != i and frozenset(s.union(s2)) not in seen:
            s3 = frozenset(s.intersection(s2))
            if len(s3) > 1:
                if s3 not in d:
                    d[s3] = 1
                else:
                    d[s3] += 1
                seen.add(frozenset(s.union(s2)))

s = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
for i in s:
    if s[i] > 2 and len(i) > 1:
        print(i, s[i])
