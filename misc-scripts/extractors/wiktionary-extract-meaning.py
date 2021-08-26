from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys
import re
import itertools

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

stopwords = open("data/stopwords/german_stopwords_full.txt", "r").read().splitlines()

input_word = sys.argv[1]
r = records[input_word][0]
if r['wikitext'].find('{{Bedeutungen}}') == -1:
    index = r['wikitext'].find('{{Grammatische Merkmale}}')
    index_end = r['wikitext'].find('\n\n', index)
    input_word = re.findall('\[\[(.*?)\]\]', r['wikitext'][index:index_end])[0]
    r = records[input_word][0]

#print(r)
index = r['wikitext'].find('{{Bedeutungen}}')
index_end = r['wikitext'].find('\n\n', index)
lines = r['wikitext'][index:index_end].splitlines()
if len(lines) > 0:
    for line in lines[1:]:
        print(line)

if len(lines) > 2:
    inputline = input('Choose meaning: ')
else:
    inputline = '1'

chosen_line = None
for line in lines:
    if inputline in line:
        chosen_line = line

word_set = set()
for word in chosen_line.split(' '):
    if word not in stopwords and ':' not in word:
        word_set.add(word.replace('[', '').replace(']', ''))

final_set = set()
final_set.add(input_word)

if re.search('^\:\[\d+\] \[\[.*\]\]$', chosen_line) != None:
    final_set = final_set.union(re.findall('\[\[(.*?)\]\]', chosen_line))

index = r['wikitext'].find('{{Synonyme}}')
index_end = r['wikitext'].find('\n\n', index)
syn_lines = r['wikitext'][index:index_end].splitlines()
syn_line = ''
for line in syn_lines:
    if inputline in line:
        syn_line += line + ' '
res = re.findall('\[\[(.*?)\]\]', syn_line)
#print(res)
final_set = final_set.union(res)

index = r['wikitext'].find('{{Sinnverwandte Wörter}}')
index_end = r['wikitext'].find('\n\n', index)
syn_lines = r['wikitext'][index:index_end].splitlines()
syn_line = ''
for line in syn_lines:
    if inputline in line:
        syn_line += line + ' '
res = re.findall('\[\[(.*?)\]\]', syn_line)
final_set = final_set.union(res)
#print(res)

for k in records.keys():
    for r in records[k]:
        index = r['wikitext'].find('{{Bedeutungen}}')
        index_end = r['wikitext'].find('\n\n', index)

        found_line = None
        lines = words = r['wikitext'][index:index_end].splitlines()
        for line in lines:
            words = line.split(' ')
            word_set2 = set()
            for word in words:
                if word in word_set and word not in stopwords:
                    word_set2.add(word.replace('[', '').replace(']', ''))
                    #print(word_set2)
            #print(word_set)
            #print(word_set2)
            if word_set.issubset(word_set2):
                line = re.sub('\'\'.*\'\'', '', line)
                res2 = re.findall('\[\[(.*?)\]\]', line)
                final_set = final_set.union(res2)
                final_set.add(k)


for k in records.keys():
    for r in records[k]:
        index = r['wikitext'].find('{{Synonyme}}')
        index_end = r['wikitext'].find('\n\n', index)

        lines = r['wikitext'][index:index_end].splitlines()
        if len(lines) > 0:
            for line in lines[1:]:
                line = re.sub('\'\'.*\'\'', '', line)
                res2 = re.findall('\[\[(.*?)\]\]', line)
                if len(res2) < 10:
                    sets = findsubsets(res, 2)
                    for s in sets:
                        t = set(s)
                        if t.issubset(res2):
                            if '[[reich]]' in line:
                                print(line)
                            #print(res2)
                            final_set = final_set.union(res2)


        index = r['wikitext'].find('{{Sinnverwandte Wörter}}')
        index_end = r['wikitext'].find('\n\n', index)

        lines = r['wikitext'][index:index_end].splitlines()
        if len(lines) > 0:
            for line in lines[1:]:
                line = re.sub('\'\'.*\'\'', '', line)
                res2 = re.findall('\[\[(.*?)\]\]', line)
                if len(res2) < 10:
                    sets = findsubsets(res, 2)
                    for s in sets:
                        t = set(s)
                        if t.issubset(res2):
                            #print(res2)
                            final_set = final_set.union(res2)

for k in final_set:
    if k in records:
        for r in records[k]:
            index = r['wikitext'].find('{{Synonyme}}')
            index_end = r['wikitext'].find('\n\n', index)

            lines = r['wikitext'][index:index_end].splitlines()
            if len(lines) > 0:
                for line in lines[1:]:
                    line = re.sub('\'\'.*\'\'', '', line)
                    res2 = re.findall('\[\[(.*?)\]\]', line)
                    if len(res2) < 10:
                        sets = findsubsets(final_set, 2)
                        for s in sets:
                            t = set(s)
                            if t.issubset(res2):
                                #print(res2)
                                final_set = final_set.union(res2)


            index = r['wikitext'].find('{{Sinnverwandte Wörter}}')
            index_end = r['wikitext'].find('\n\n', index)

            lines = r['wikitext'][index:index_end].splitlines()
            if len(lines) > 0:
                for line in lines[1:]:
                    line = re.sub('\'\'.*\'\'', '', line)
                    res2 = re.findall('\[\[(.*?)\]\]', line)
                    if len(res2) < 10:
                        sets = findsubsets(final_set, 2)
                        for s in sets:
                            t = set(s)
                            if t.issubset(res2):
                                #if '[[reich]]' in line:
                                #    print(k)
                                #print(k)
                                #print(res2)
                                #if c > 10:
                                final_set = final_set.union(res2)


#final_set2 = set()
#r = records[input_word][0]
#wortart = re.findall('Wortart\|(\w+)\|', r['wikitext'])[0]
#for k in final_set:
#    if k in records:
#        for r in records[k]:
#            res = re.findall('Wortart\|(\w+)\|', r['wikitext'])
#            if len(res) == 1 and res[0] == wortart:
#                final_set2.add(k)



rm_list = [
    ':',
    'schriftsprachlich'
]

final_set3 = set()
for fs in final_set:
    found = False
    for rm in rm_list:
        if rm in fs:
            found = True
    if found == False:
        final_set3.add(fs)
print(final_set3)
