from bz2file import BZ2File
from wiktionary_de_parser import Parser
import json
import sys
import re
import itertools
import os

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

f = open("wiktionary-lookupable.txt", "r")
records = json.loads(f.read())
f.close()

stopwords = open("data/stopwords/german_stopwords_full.txt", "r").read().splitlines()

final_set_complete = set()
seen_set = set()

first_inputline = None

input_word = sys.argv[1]

def find_words(input_word):
    if input_word not in records:
        return set()
    r = records[input_word][0]

    #print(r)
    index = r['wikitext'].find('{{Bedeutungen}}')
    index_end = r['wikitext'].find('\n\n', index)
    lines = r['wikitext'][index:index_end].splitlines()
    print(':[0] nicht gelistet, überspringen')
    if len(lines) > 0:
        for line in lines[1:]:
            print(line)

    inputline = input('Choose meaning for word "' + input_word + '": ')
    if inputline == '0':
        return set()

    global first_inputline
    if first_inputline == None:
        first_inputline = inputline

    folder_name = sys.argv[1] + "_" + first_inputline
    if os.path.exists(folder_name) == False:
        os.mkdir(folder_name)
    if os.path.exists(os.path.join(folder_name, 'opposite')) == False:
        os.mkdir(os.path.join(folder_name, 'opposite'))

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
    syn_line = re.sub('\'\'.*\'\'', '', syn_line)
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
    syn_line = re.sub('\'\'.*\'\'', '', syn_line)
    res = re.findall('\[\[(.*?)\]\]', syn_line)
    final_set = final_set.union(res)
    #print(res)

    final_set2 = set()
    r = records[input_word][0]
    wortart = re.findall('Wortart\|(\w+)\|', r['wikitext'])[0]
    for k in final_set:
        if k in records:
            for r in records[k]:
                res = re.findall('Wortart\|(\w+)\|', r['wikitext'])
                if len(res) == 1 and res[0] == wortart:
                    final_set2.add(k)

    rm_list = [
        ':',
        'schriftsprachlich',
        'umgangssprachlich'
    ]

    final_set3 = set()
    for fs in final_set2:
        found = False
        for rm in rm_list:
            if rm in fs:
                found = True
        if found == False:
            final_set3.add(fs)

    f = open(os.path.join(folder_name, input_word + "_" + inputline + ".txt"), "w")
    for o in final_set3:
        f.write(o + "\n")
    f.close()

    opp_set = set()
    index = r['wikitext'].find('{{Gegenwörter}}')
    index_end = r['wikitext'].find('\n\n', index)
    syn_lines = r['wikitext'][index:index_end].splitlines()
    syn_line = ''
    for line in syn_lines:
        if inputline in line:
            syn_line += line + ' '
    syn_line = re.sub('\'\'.*\'\'', '', syn_line)
    res = re.findall('\[\[(.*?)\]\]', syn_line)
    #print(res)
    opp_set = set(res)
    f = open(os.path.join(folder_name, 'opposite', input_word + "_" + inputline + ".txt"), "w")
    for o in opp_set:
        f.write(o + "\n")
    f.close()

    print('Opposites:')
    print(opp_set)

    return final_set3


while len(final_set_complete) == 0 or len(final_set_complete.difference(seen_set)) != 0:
    print('')
    if len(final_set_complete) == 0:
        w = sys.argv[1]
    else:
        remaining_words = final_set_complete.difference(seen_set)
        #print(remaining_words)
        w = next(iter(remaining_words))

    final_set_complete = final_set_complete.union(find_words(w))
    final_set_complete.add(w)
    seen_set.add(w)
    print('')
    print(final_set_complete)
