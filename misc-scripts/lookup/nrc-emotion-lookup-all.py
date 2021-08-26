import os
import sys
from langdetect import detect

def hasupper(w):
    s = w.split(' ')
    for w in s:
        if len(w) > 0 and w[0].isupper():
            return True
    return False

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def main():

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

    s = set()
    i = 0
    for line in open(sys.argv[1], encoding="utf8").read().splitlines():
        i = i + 1
        if i == 1:
            continue
        splitted = line.split('\t')
        #print(splitted)
        if splitted[0] in d:
            for w in d[splitted[0]]:
                if hasupper(w) == False:
                    print(w + '\t' + splitted[0] + '\t' + splitted[1] + '\t' + splitted[2])
            #print()

        #v = float(splitted[len(splitted) - 1])
        #if len(splitted) == 3:
        #    if splitted[1] == sys.argv[2]:
                #sys.stdout.buffer.write((splitted[0] + '\n').encode('utf8'))
        #else:
        #    if splitted[2] == sys.argv[2] and splitted[1] != 'NO TRANSLATION':
        #        sys.stdout.buffer.write((splitted[1] + '\n').encode('utf8'))

if __name__ == "__main__":
    main()
