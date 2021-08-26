from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys
import re

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

k = sys.argv[1]
if k in records:
    r = records[k][0]
    lines = r['wikitext'].splitlines()
    for line in lines:
        if 'Plural' in line:
            res = re.findall('\=(.*)', line)
            print(res)
