from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

w = sys.argv[1]
ftype = sys.argv[2]

flexion = set()

def lookup(c):
    if ftype == "verb" and 'Präsens_ich' in c['flexion']:
        for k in c['flexion']:
            if k != 'Hilfsverb':
                flexion.add(c['flexion'][k])
    elif ftype == "adj" and 'Komparativ' in c['flexion']:
        for k in c['flexion']:
            flexion.add(c['flexion'][k])

for c in records[w]:
    if 'flexion' not in c:
        if 'lemma' in c:
            w2 = c['lemma']
            for c2 in records[w2]:
                if 'flexion' in c2:
                    lookup(c2)
    else:
        lookup(c)

for s in flexion:
    print(s)
