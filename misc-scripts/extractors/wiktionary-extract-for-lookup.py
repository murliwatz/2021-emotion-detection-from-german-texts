### transforms wiktionary in a lookupable json file ###

from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json

bzfile_path = '/Users/paulproll/Downloads/dewiktionary-latest-pages-meta-current.xml.bz2'
bz = BZ2File(bzfile_path)

d = {}

for record in Parser(bz):
    if 'langCode' not in record or record['langCode'] != 'de':
      continue

    # do stuff with 'record'
    if record['title'] in d:
        d[record['title']].append(record)
    else:
        d[record['title']] = [record]

json2 = json.dumps(d)

f = open("wiktionary-lookupable.txt", "w")
f.write(json2)
f.close()
