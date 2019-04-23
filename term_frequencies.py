"""
This Python script is used to analyze term frequencies.
"""
import operator
import json
from collections import Counter
import pre_process
from nltk.corpus import stopwords
from nltk import bigrams
import string


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ["rt", "via"]

fname = "data/stream_trump.json"
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        ppterms = pre_process.preprocess(tweet['text'])
        terms_all = [term for term in ppterms]
        terms_stop = [term for term in ppterms if term not in stop]
        terms_single = set(terms_all)
        terms_hash = [term for term in ppterms if term.startswith('#')]
        terms_only = [term for term in ppterms if term not in stop and not term.startswith(('#', '@'))]
        terms_bigram = bigrams(terms_stop)
        count_all.update(terms_bigram)
    print(count_all.most_common(5))
