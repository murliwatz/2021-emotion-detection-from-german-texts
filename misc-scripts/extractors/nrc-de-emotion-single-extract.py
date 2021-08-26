import os
import sys

threshold = 0.8

def main():
    s = set()
    i = 0
    for line in open(sys.argv[1], encoding="utf8").read().splitlines():
        i = i + 1
        if i == 1:
            continue
        splitted = line.split('\t')
        v = float(splitted[len(splitted) - 1])
        if v > threshold:
            if len(splitted) == 3:
                if splitted[1] == sys.argv[2]:
                    sys.stdout.buffer.write((splitted[0] + '\n').encode('utf8'))
            else:
                if splitted[2] == sys.argv[2] and splitted[1] != 'NO TRANSLATION':
                    sys.stdout.buffer.write((splitted[1] + '\n').encode('utf8'))

if __name__ == "__main__":
    main()
