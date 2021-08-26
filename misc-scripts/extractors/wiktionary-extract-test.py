from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

print(records[sys.argv[1]])
