import os
import sys
import re

def main():
    with open(sys.argv[1], encoding="utf8") as f:
        #regex = re.compile(".*?\((.*?)\)")
        pos = ['adj', 'noun', 'conj', 'verb', 'pron']
        for line in f:
            splitted = line.split("\t")
            if len(splitted) <= 2:
                continue
            str = splitted[0]
            result = re.sub("\((.*?)\)", "", str)
            result = re.sub("\{(.*?)\}", "", result)
            result = re.sub("\[(.*?)\]", "", result)
            result = re.sub("\<(.*?)\>", "", result)
            for p in pos:
                if p in line:
                    sys.stdout.buffer.write((result.rstrip(' ').lstrip(' ') + '\t' + p + '\n').encode('utf8'))


if __name__ == "__main__":
    main()
