import sys
import os

from os import listdir
from os.path import isfile, join


files = []
if os.path.isdir(sys.argv[1]):
    files = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
else:
    files = [sys.argv[1]]

dict_file = open(sys.argv[2], encoding="utf8")

d = dict()

for w in dict_file.read().splitlines():
    ws = w.split("\t")
    if len(ws) == 2:
        w1 = ws[0]
        w2 = ws[1].lower()
        if w2 in d:
            d[w2].append(w1)
        else:
            d[w2] = [w1]

for file in files:
    words_file = open(join(sys.argv[1], file), encoding="utf8")
    print(file)

    s = set()
    for w in words_file.read().splitlines():
        wl = w.lower()
        if wl in d:
            s.add('\n'.join(d[wl]))
    print(s)

    f = open(join(sys.argv[3], file), "w", encoding="utf-8")
    for e in s:
        f.write(e + "\n")
    f.close()
        #sys.stdout.buffer.write((e + "\n").encode('utf8'))
