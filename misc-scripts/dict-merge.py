import sys

words = open(sys.argv[1], encoding="utf8").read().splitlines()
words2 = open(sys.argv[2], encoding="utf8").read().splitlines()

s = set()

for w in words:
    s.add(w)
for w in words2:
    s.add(w)

s = sorted(s)

for w in s:
    sys.stdout.buffer.write((w + "\n").encode('utf8'))
