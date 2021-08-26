import sys
import re

lines = open(sys.argv[1], encoding="utf8").read().splitlines()

for line in lines:
    if len(line) > 0 and line[0].isupper():
        print(line)
