from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys
import re

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

s = set()

for line in open(sys.argv[1], encoding="utf8").read().splitlines():
    w = line
    s.add(w)
    if w in records:
        r = records[w][0]
        lines = r['wikitext'].splitlines()
        for line in lines:
            if 'Plural' in line:
                res = re.findall('\=(.*)', line)
                if len(res) > 0 and '[' not in res[0]:
                    s.add(res[0])

for e in sorted(s):
    print(e)
