import spacy
import sys
import os
import yaml
import copy
import re

show_no_matches = False
debug = False
debug_verbose = False
#emotion_dir = 'data/emotions/generated/github-attreyabhatt/de-translated-extended/spacy-lemma/'
emotion_dir = 'emotions/generated/'
synonym_dir = 'synonyms/lemmatized'
flexions_dir = 'flexions'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

nlp = spacy.load('de_core_news_lg')

rule_files_parsed = []

if os.path.isdir(sys.argv[1]):
    flist = os.listdir(sys.argv[1])
    for file in flist:
        path = os.path.join(sys.argv[1], file)
        if os.path.isfile(path):
            yaml_file = open(path, 'r',encoding="utf8")
            parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
            rule_files_parsed.append(parsed_yaml_file)
else:
    yaml_file = open(sys.argv[1], 'r', encoding="utf8")
    parsed_yaml_file = yaml.load(yaml_file, Loader=yaml.FullLoader)
    rule_files_parsed = [parsed_yaml_file]

file_cache = dict()

def main():

    samples = []
    if len(sys.argv) == 2:
        samples = sys.stdin.readlines()
    else:
        samples = open(sys.argv[2], encoding="utf8").read().splitlines()

    rules_compiled = []

    for read_rules in rule_files_parsed:
        n = 0
        for r in read_rules['RULES']:
            regex = convert_rule_to_regex(r)
            rules_compiled.append({
                'regex_clear': regex,
				'regex': re.compile(regex),
				'class': read_rules['CLASS'],
                'num': n
			})
            n += 1

    count = 0
    annotated_count = 0
    matched_count = 0
    mismatch_count = 0
    no_annotation_matched_count = 0
    for sample in samples:
        s = sample.split("\t")
        sen = s[0]
        annotation = '**no annotation**'
        if len(s) == 2:
            annotation = s[1]
        if len(s) == 3:
            annotation = s[1] + ' ' + s[2]
        if debug:
            print('###', sen.rstrip(), '###')
        doc = nlp(sen)
        result = '\n'.join([x.lemma_.lower() + "\t" + x.pos_ + "\t" + x.tag_ for x in doc])
        token_string = create_token_string(doc)
        if debug or len(samples) == 1:
            print(token_string)

        matched = False

        for h in rules_compiled:
            match = h['regex'].search(token_string)
            if match is not None:
                print(match.group())
                matched = True
                count = count + 1
                if annotation == '**no annotation**':
                    no_annotation_matched_count += 1
                if annotation != '**no annotation**':
                    annotated_count += 1
                col = bcolors.WARNING
                if h['class'] == annotation:
                    col = bcolors.OKGREEN
                    matched_count += 1
                elif h['class'] != annotation and annotation != '**no annotation**':
                    col = bcolors.FAIL
                    mismatch_count += 1
                #print(h['regex_clear'])
                print(col, '+++:', sen.rstrip(), '\tACTUAL:' , h['class'] , '/ EXPECTED:', annotation, '(', h['num'], ')')
                print('')
                break
        if matched == False and show_no_matches:
            print('---:', sen)
    print('')
    print(no_annotation_matched_count, "of", count, "matches don't have annotations!")
    print(matched_count, "of", count, "sentences are matched correctly!")
    print(mismatch_count, "of", count, "sentences are matched incorrectly!")
    print(count, "of", len(samples), "sentences matched!")

def create_token_string(doc):
    str = ''
    for t in doc:
        str = str + t.text + "{" + t.lemma_.lower() + "/" + t.pos_ + "/" + t.tag_ + "}"
    return str

def convert_rule_to_regex(rule):
    regex = ''
    for r in rule:
        regex = regex + convert_subrule_to_regex(r)
    #placeholder = '[a-zA-Z0-9!$,.?äöüß\']*'
    #regex = '(^|' + placeholder + '\\{' + placeholder + '\\/PUNCT\\/' + placeholder + '\\})' + regex
    return regex

def convert_subrule_to_regex(c_rule):
    placeholder = '[a-zA-Z0-9!$,.?äöüß\']*'
    regex = '%word%\{%lemma%\/%pos%\/%tag%\}'
    for key in c_rule.keys():
        if key == 'OR':
            sub_regex = []
            for sub_rule in c_rule[key]:
                res = convert_subrule_to_regex(sub_rule)
                sub_regex.append(res)
            regex = '(' + '|'.join(sub_regex) + ')'
        if key == 'POS':
            if isinstance(c_rule[key], str):
                regex = regex.replace('%pos%', c_rule[key])
            elif isinstance(c_rule[key], list):
                regex = regex.replace('%pos%', '(' + '|'.join(c_rule[key]) + ')')
        if key == 'ANY':
            regex = '[a-zA-Z0-9!$,.?äöüß\{\}\/\']*'
        if key == 'WORD':
            if isinstance(c_rule[key], str):
                regex = regex.replace('%word%', '[' + c_rule[key][0].lower() + '|' + c_rule[key][0].upper() + ']' + c_rule[key][1:].lower())
            elif isinstance(c_rule[key], list):
                lst = []
                for l in c_rule[key]:
                    lst.append('[' + l[0].lower() + '|' + l[0].upper() + ']' + l[1:])
                regex = regex.replace('%word%', '(' + '|'.join(lst) + ')')
        if key == 'TAG':
            regex = regex.replace('%tag%', c_rule[key])
        if key == 'OPT':
            regex = '(' + regex + '|' + placeholder + ')'
        if key == 'LEMMA':
            if isinstance(c_rule[key], str):
                regex = regex.replace('%lemma%', c_rule[key].lower())
            elif isinstance(c_rule[key], list):
                regex = regex.replace('%lemma%', '(' + '|'.join(c_rule[key]).lower() + ')')
            elif isinstance(c_rule[key], dict):
                dir = emotion_dir
                if 'TYPE' in c_rule[key] and c_rule[key]["TYPE"] == 'SYN':
                    dir = synonym_dir
                if 'TYPE' in c_rule[key] and c_rule[key]["TYPE"] == 'FLEXION':
                    dir = flexions_dir
                path = os.path.join(dir,c_rule[key]["FILE"])
                tokens = []
                if path in file_cache:
                    tokens = file_cache[path]
                else:
                    lines = open(path, encoding="utf8").read().splitlines()
                    ext = ['', 'e', 'er', 'en', 'es']
                    for line in lines:
                        if re.match('[A-Za-zäöüß\-]', line) != None:
                            if line.strip() == '':
                                continue
                            for e in ext:
                                tokens.append(line.strip() + e)
                        #tokens.append(nlp(line)[0].lemma_)
                regex = regex.replace('%lemma%', '(' + '|'.join(tokens).lower() + ')')
    regex = regex.replace('%pos%', placeholder)
    regex = regex.replace('%tag%', placeholder)
    regex = regex.replace('%lemma%', placeholder)
    regex = regex.replace('%word%', placeholder)
    return regex

def create_opt_rules(rule):
    return create_opt_rules_rec(0, 0, rule)

def create_opt_rules_rec(rec_index, index, rule):
    rule = copy.deepcopy(rule)
    rules = [rule]
    for i in range(index, len(rule)):
        if 'OPT' in rule[i] and rule[i]['OPT']:
            new_rule = rule[:i] + rule[i+1:]
            del rule[i]['OPT']
            if debug and debug_verbose:
                print(rec_index, i, new_rule)
            rules.append(new_rule)
            r = create_opt_rules_rec(rec_index + 1, i, new_rule)
    return rules

if __name__ == "__main__":
    main()
