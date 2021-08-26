from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys
import re

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

for k in records.keys():
    for r in records[k]:
        index = r['wikitext'].find('{{Bedeutungen}}')
        index_end = r['wikitext'].find('\n\n', index)
        index2 = r['wikitext'].find('{{Redewendungen}}')
        index_end2 = r['wikitext'].find('\n\n', index)
        if 'Schimpfwort' in r['wikitext'][index:index_end] or 'Schimpfwort' in r['wikitext'][index2:index_end2]:
            print(k)
