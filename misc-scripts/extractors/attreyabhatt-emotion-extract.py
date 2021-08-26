import os
import sys

# Anger;Disgust;Joy;Sad;Surprise ;Fear

d = {}

def main():
    s = set()
    i = 0
    for line in open(sys.argv[1], encoding="utf8").read().splitlines():
        line = line.replace(',', '')
        line = line.replace("'", '')
        line = line.lstrip().rstrip()
        word, emotion = line.split(':')
        word = word.lstrip().rstrip()
        emotion = emotion.lstrip().rstrip()
        if emotion in d:
            d[emotion].append(word)
        else:
            d[emotion] = [word]
    for key in d.keys():
        f = open(sys.argv[2] + "\\" + key + ".txt", "w")
        f.write('\n'.join(d[key]))
        f.close()


if __name__ == "__main__":
    main()
