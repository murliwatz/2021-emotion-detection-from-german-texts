import sys

from os import listdir
from os.path import isfile, join

mypath = sys.argv[1]

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

s = set()
for filename in onlyfiles:
    words = open(join(mypath, filename), encoding="utf8").read().splitlines()
    for w in words:
        s.add(w)

s = sorted(s)
s2 = set()

for s_ in s:
    for file in onlyfiles:
        if s_ in file:
            s2.add(s_)


for w in s2:
    sys.stdout.buffer.write((w + "\n").encode('utf8'))
