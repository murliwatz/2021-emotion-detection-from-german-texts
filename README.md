
# Folder Structure

In this repository there are scripts to work with datasets and dictionaries. The idea is to have small scripts for every purpose which can be piped via stdin / stdout then. Scripts mainly have self-explanary file names. The folders are structured as followed:

- meaning-crawler: Includes the meaning crawler script
- rbs: Includes my own written rule based system based on tokenization and regex
  - rbs/rbs.py: The rule based system script
  - rbs/datasets: Datasets which are applied by the rbs
  - rbs/rules: Defined rules for the rbs
- misc-scripts: Contains several scripts used for trying out different stuff
  - misc-scripts/extractors: Scripts used to extract special data from dictionaries or datasets (words, pos, emotional words, ...)
	- misc-scripts/lemmatizer: Scripts used to lemmatize wordlists
	- misc-scripts/lookup: Scripts used to lookup words from files (especially for translation)
	- misc-scripts/stemmer: Scripts used to stemm wordlists
	- misc-scripts/triangulator: Scripts to triangulate language files

# Meaning Crawler

The crawler goes through wiktionary with the goal to get a list of words having the same meaning. All you need is to start with an initial word. You will be asked for which meaning / context you want to extract. Based on the chosen meaning the crawler looks for synonyms and related words and adds them to a queue. The queue is processed by asking for meanings until all words are processed.

At each step all synonyms, related words and even counterwords are stored in files so that they can be filtered out again and can be merged to a whole list aftwerwards (check folder Idiot_1 for instance, mostly swear words for contempt class)

## Preparation
In order to use the crawler you first have to prepare the wiktionary which can be downloaded here: https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-meta-current.xml.bz2

Change the path in the script to the path where the downloaded wiktionary is located and execute it:
```
rbs/extractors/wiktionary-extract-for-lookup.py
```

## How to use the crawler
```
meaning-crawler/wiktionary-extract-meaning-crawler.py Unsinn
```

```
:[0] nicht gelistet, überspringen
:[1] etwas, das [[kein]]en [[Sinn]] hat
:[2] [[unüberlegt]]e [[Handlung]]
Choose meaning for word "Unsinn":
```
```
Input: 1
```
New words in set:

{'Quatsch', 'Schwachsinn', 'Käse', 'Unfug', 'Stuss', 'Galimathias', 'Mumpitz', 'Dummheit', 'Mist', 'Wahnwitz', 'Blödsinn', 'Blech', 'Nonsens', 'Firlefanz', 'Unsinn', 'Humbug', 'Kokolores', 'Irrsinn', 'Larifari', 'Wahnsinn', 'Schnickschnack'}

```
:[0] nicht gelistet, überspringen
:[1] dumme, [[ungereimt]]e Aussage
:[2] [[Torheit]], falsche, unüberlegte, unkluge Handlung
:[3] [[Alberei]], kindisches Benehmen
:[4] etwas Unsinniges
:[5] breiiger Matsch

Choose meaning for word "Quatsch":
```
```
Input: 4
```
No added synonyms / related words added:


{'Quatsch', 'Schwachsinn', 'Käse', 'Unfug', 'Stuss', 'Galimathias', 'Mumpitz', 'Dummheit', 'Mist', 'Wahnwitz', 'Blödsinn', 'Blech', 'Nonsens', 'Firlefanz', 'Unsinn', 'Humbug', 'Kokolores', 'Irrsinn', 'Larifari', 'Wahnsinn', 'Schnickschnack'}

```
:[0] nicht gelistet, überspringen
:[1] {{K|Medizin|Psychiatrie|veraltend}} Geistige Behinderung: [[Intelligenzquotient]] von unter 70
:[2] {{K|umgangssprachlich}} etwas Unsinniges
Choose meaning for word "Schwachsinn":
```
```
Input: 2
```
Changed set:

{'Quatsch', 'Schwachsinn', 'Käse', 'Unfug', 'Stuss', 'Galimathias', 'Mumpitz', 'Dummheit', 'Mist', 'Wahnwitz', 'Blödsinn', 'Blech', 'Nonsens', 'Firlefanz', 'Unsinn', 'Schrott', 'Humbug', 'Kokolores', 'Irrsinn', 'Scheißdreck', 'Larifari', 'Wahnsinn', 'Schnickschnack'}

```
:[0] nicht gelistet, überspringen
:[1] ein festes [[Milchprodukt]]
:[2] ''regional:'' [[Quark]], ''vor allem in Verbindungen wie'' [[Käsekuchen]], [[Käsetorte]]
:[3] ''umgangssprachlich:'' Unsinn, Unrealistisches, Unwahres
Choose meaning for word "Käse":
```
```
Input: 3
```
...

# Merge crawler lists to one list

This tool sorts out skipped words from crawler and creates a whole word list

```
misc-scripts/crawler-merge-list.py ./Idiot_1/
```

# Extract plurals for nouns

Spacy (which is used to tokenize and lemmatize words in my rule based system) does a good job in lemmatization, but swear words like "Arschlöcher" can't be lemmatized correctly for instance. So the idea is to extract plural forms of nouns and add them to the word list as well.

```
misc-scripts/extractors/wiktionary-extract-plural.py Arschloch
```

Output:
```
Arschlöcher
Arschlöchern
```

The same is possible for a whole word list:

```
misc-scripts/extractors/wiktionary-extract-plural-list.py Idiot_1.txt
```

Output:
```
Aas
Aase
Aasen
Affe
Affen
Angeber
Angebern
Angsthase
Angsthasen
Armleuchter
Armleuchtern
Arsch
Arschgeige
Arschgeigen
Arschgesicht
Arschgesichter
Arschgesichtern
Arschloch
Arschlöcher
Arschlöchern
Bandit
Banditen
...
```

# Rule Based System

The rule-based system is lexical-based method: The idea is to combine a rule-based system with a pre-trained NLP model to filter specific sequences of text and then assert them. In this chapter, some NLP concepts are explained and how they are used in the rule-based system.

The advantage of this method is that, in contrast to methods that use weighted keywords only, for example, the context of the words is known, so that more accurate results may be obtained.

## Writing rulesets

Write rules via yaml files:
Examples in rbs/rules

Example of a ruleset:
```yaml
CLASS: BORING
NAME: 'Some boring rules'
RULES:
-
  - LEMMA: sein
  - OR: [ { POS: AUX }, { POS: ADV }, { POS: PRON }]
    OPT: True
  - OR: [ { POS: AUX }, { POS: ADV }, { POS: PRON }]
  - LEMMA:
      FILE: 'bored.txt'
-
  - POS: VERB
  - POS: ADJ
    OPT: True
  - LEMMA: { FILE: 'bored.txt' }
  - OR: [ {TAG: PTKVZ}, {TAG: APPR } ]
    OPT: True
```

Example of annotated file:
```
Na ja , es gibt kein Zurück .
Sieh mich an , wir können doch reden .
Ich kann es nicht mehr sehen .	ANGER
Was kannst du nicht mehr sehen ?
Mich !
Hör zu , wir reden einfach darüber , dann klären wir das .
- Ich tu , was immer du willst , versprochen .
- Halt die Schnauze !	ANGER
- Höre mir doch einfach zu . ANGER
- Du weißt gar nichts !	ANGER
Ich verstehe nicht , wieso du das tust !	ANGER
Bitte !
Binde mich hier los !
Binde mich von dem verfickten Ding los !	ANGER
Fuck !
Fuck .
Fuck .
```

## Usage

Take all rules / all yaml files from a folder and run it over an ANNOTATED sample file:
```
python rbs_v3.py rules\tone-analysis\ datasets\tone-analysis\de_sample_annotated.txt
```

OR:

Take rules from one yaml file and run it over an ANNOTATED sample file:
```
python rbs\rbs_v3.py rbs\rules\tone-analysis\hated.txt rbs\datasets\tone-analysis\de_sample_annotated.txt
```

OR:

Take rules and run it over a single sentence:
```
echo Du verfickte Hure! | python rbs\rbs_v3.py rbs\rules\tone-analysis\hated.txt
```

## Example with GermEval2018 dataset

Applying insult rules to the germeval insult training set
```
python rbs.py rules/germeval2018/insult.yaml datasets/GermEval2018/cleaned/germeval2018.training.insult_offense.txt
```

Applying insult rules to the whole germeval test set
```
python rbs.py rules/germeval2018/insult.yaml datasets/GermEval2018/germeval2018.test_offense.txt
```
