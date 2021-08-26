import os
import sys

# Anger;Disgust;Joy;Sad;Surprise ;Fear

d = []

def main():
    s = set()
    i = 0
    for line in open(sys.argv[1], encoding="utf8").read().splitlines():
        i = i + 1
        if i == 1:
            continue
        splitted = line.split(';')
        emotion_index = 0
        if sys.argv[2] == 'anger':
            emotion_index = 1
        elif sys.argv[2] == 'disgust':
            emotion_index = 2
        elif sys.argv[2] == 'joy':
            emotion_index = 3
        elif sys.argv[2] == 'sad':
            emotion_index = 4
        elif sys.argv[2] == 'surprise':
            emotion_index = 5
        elif sys.argv[2] == 'fear':
            emotion_index = 6
        if emotion_index > 0:
            if splitted[emotion_index] == '1':
                sys.stdout.buffer.write((splitted[0].replace('_', ' ') + '\n').encode('utf8'))

if __name__ == "__main__":
    main()
