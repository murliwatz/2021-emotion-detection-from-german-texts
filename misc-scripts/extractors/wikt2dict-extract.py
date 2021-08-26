import os
import sys

def main():
    s = set()
    with open(sys.argv[1], encoding="utf8") as f:
        for line in f:
            list = []
            values = line.split("\t")
            added = ""
            for i in range(len(values)):
                if values[i] == 'de' and added != "de":
                    list.append(('de', values[i + 1].rstrip("\n")))
                    added = "de"
                if values[i] == 'en' and added != "en":
                    list.append(('en', values[i + 1].rstrip("\n")))
                    added = "en"
            fs = frozenset(list)
            s.add(fs)
    for x in s:
        if len(x) > 2 or len(x) < 2:
            continue
        #print(x)
        str = "\t"
        for x2 in x:
            if 'de' in x2:
                str = x2[1] + str
            if 'en' in x2:
                str = str + x2[1]
        str = str + "\n"
        sys.stdout.buffer.write(str.encode('utf8'))

if __name__ == "__main__":
    main()
