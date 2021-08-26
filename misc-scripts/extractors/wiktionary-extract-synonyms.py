from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys
import re

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

pos = None

if sys.argv[1] in records.keys():
    for r in records[sys.argv[1]]:
        if 'pos' in r.keys() and len(r['pos'].keys()) > 0:
            pos = list(r['pos'].keys())[0]

for k in records.keys():
    for r in records[k]:
        index = r['wikitext'].find('{{Synonyme}}')
        index_end = r['wikitext'].find('\n\n', index)
        if k == sys.argv[1] or ('pos' in r.keys() and pos in r['pos'].keys() and "[[" + sys.argv[1] + "]]" in r['wikitext'][index:index_end]):
            syn_lines = r['wikitext'][index:index_end].splitlines()
            for syn_line in syn_lines:
                if k == sys.argv[1] or "[[" + sys.argv[1] + "]]" in syn_line:
                    res = re.findall('\[\[(.*?)\]\]', syn_line)
                    if len(res) < 6:
                        print(k)
                        print(res)
