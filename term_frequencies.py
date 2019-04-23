"""
This Python script is used to analyze term frequencies.
"""
import operator
import json
from collections import Counter
import pre_process
from nltk.corpus import stopwords
import string

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ["rt", "via"]

fname = "data/stream_youtube.json"
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        terms_stop = [term for term in pre_process.preprocess(tweet['text']) if term not in stop]
        count_all.update(terms_stop)
    print(count_all.most_common(5))
