import treetaggerwrapper
import nltk
from pprint import pprint

tree_tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')

sent = "Das ist schon sehr schön mit den Expertinnen und Experten."

words = nltk.word_tokenize(sent)
tags = tree_tagger.tag_text(words,tagonly=True) #don't use the TreeTagger's tokenization!
nice_tags = treetaggerwrapper.make_tags(tags)
pprint(nice_tags)
