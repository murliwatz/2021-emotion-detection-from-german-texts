import sys
import re

lines = open(sys.argv[1], encoding="utf8").read().splitlines()

for line in lines:
    line = re.sub('@\w+ ', ' ', line)
    line = line.replace('#', '')
    line = line.strip()
    print(line)
