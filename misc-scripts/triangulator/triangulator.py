import sys
import base64

words = open(sys.argv[1], encoding="utf8").read().splitlines()
words2 = open(sys.argv[2], encoding="utf8").read().splitlines()

ws_array = []
for w in words:
    ws_array.append(w.split('\t'))

ws_array2 = []
for w in words2:
    ws_array2.append(w.split('\t'))

for w in ws_array:
    for w2 in ws_array2:
        if w[1] == w2[0]:
            sys.stdout.buffer.write((w[0] + "\t" + w2[1] + "\n").encode('utf8'))
