from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

flexion = set()

def lookup(c):
    if 'Präsens_ich' in c['flexion']:
        for k in c['flexion']:
            if k != 'Hilfsverb' and c['flexion'][k] != 'haben' and c['flexion'][k] != 'sein':
                flexion.add(c['flexion'][k])
    elif 'Komparativ' in c['flexion']:
        for k in c['flexion']:
            flexion.add(c['flexion'][k])

for line in open(sys.argv[1], encoding="utf8").read().splitlines():
    w = line
    flexion.add(w)
    if w in records:
        for c in records[w]:
            #print(c)
            if 'flexion' not in c:
                if 'lemma' in c:
                    w2 = c['lemma']
                    for c2 in records[w2]:
                        if 'flexion' in c2:
                            lookup(c2)
            else:
                lookup(c)

if None in flexion:
    flexion.remove(None)
for e in sorted(flexion):
    sys.stdout.buffer.write((e + '\n').encode('utf8'))
