import sys

words = set(open(sys.argv[1], encoding="utf8").read().splitlines())
words2 = set(open(sys.argv[2], encoding="utf8").read().splitlines())

s = set()

s = s.union(words - words2)
s = s.union(words2 - words)

s = sorted(s)

for w in s:
    sys.stdout.buffer.write((w + "\n").encode('utf8'))
