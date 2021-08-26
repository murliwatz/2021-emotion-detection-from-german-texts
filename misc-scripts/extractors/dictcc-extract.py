import os
import sys
import re

def main():
    with open(sys.argv[1], encoding="utf8") as f:
        #regex = re.compile(".*?\((.*?)\)")
        for line in f:
            splitted = line.split("\t")
            if len(splitted) <= 2:
                continue
            str = splitted[0] + "\t" + splitted[1]
            result = re.sub("\((.*?)\)", "", str)
            result = re.sub("\{(.*?)\}", "", result)
            result = re.sub("\[(.*?)\]", "", result)
            result = re.sub("\<(.*?)\>", "", result)
            splitted = result.split("\t")
            if len(splitted) < 2:
                continue
            result = splitted[0].lstrip(' ').rstrip(' ') + "\t" + splitted[1].lstrip(' ').rstrip(' ') + "\n"
            sys.stdout.buffer.write(result.encode('utf8'))

if __name__ == "__main__":
    main()
