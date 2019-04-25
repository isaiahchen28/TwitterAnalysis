"""
This Python script is used to analyze term frequencies.
"""
import string
from nltk import bigrams
from nltk.corpus import stopwords
from collections import Counter
from collections import defaultdict
import json
import pre_process
import operator


def generate_term_list(filename, term_filter):
    """
    Generate list of terms
    """
    # Define list of common characters used for punctuation
    punctuation = list(string.punctuation)
    # Define list of stop-words, which are common words that do not carry
    # significance (conjunctions, adverbs, etc.)
    stop = stopwords.words('english') + punctuation + ["rt", "via"]
    terms = []
    # Open the file
    with open(filename, 'r') as f:
        # Parse through each line/Tweet in the .json file
        for line in f:
            tweet = json.loads(line)
            # Pre-process the information in the Tweet
            ppterms = pre_process.preprocess(tweet['text'])
            # Apply the appropriate filter as specified by the user
            if term_filter == "remove_stop_words":
                terms.append([term for term in ppterms if term not in stop])
            elif term_filter == "hashtags":
                terms.append(
                    [term for term in ppterms if term.startswith('#')])
            elif term_filter == "terms_only":
                terms.append(
                    [term for term in ppterms if term not in stop and not term.startswith(('#', '@'))])
            elif term_filter == "single_terms":
                temp = [term for term in ppterms]
                terms.append(set(temp))
            elif term_filter == "default" or term_filter is None:
                terms.append([term for term in ppterms])
            else:
                raise Exception("Invalid filter type.")
    return terms


def calculate_term_frequencies(term_list, n):
    """
    Calculate term frequencies
    """
    count_all = Counter()
    for i in term_list:
        count_all.update(i)
    return count_all.most_common(n)


def term_co_occurrences(term_list, n):
    """
    Calculate the number of term co-occurences
    """
    com = defaultdict(lambda: defaultdict(int))
    for tweet in term_list:
        # Build co-occurrence matrix
        for i in range(len(tweet) - 1):
            for j in range(i + 1, len(tweet)):
                w1, w2 = sorted([tweet[i], tweet[j]])
                if w1 != w2:
                    com[w1][w2] += 1
    com_max = []
    for t1 in com:
        t1_max_terms = sorted(
            com[t1].items(), key=operator.itemgetter(1), reverse=True)[:n]
        for t2, count in t1_max_terms:
            com_max.append(((t1, t2), count))
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    return terms_max[:n]

def search_word_co_occurrences(keyword, term_list, n):
    """
    Calculate term co-occurrences for a given keyword
    """
    count_search = Counter()
    for tweet in term_list:
        if keyword in tweet:
            count_search.update(tweet)
    return count_search.most_common(n)



if __name__ == '__main__':
    filename = "data/stream_biden.json"
    term_filter = "terms_only"
    terms = generate_term_list(filename, term_filter)
    # common_terms = calculate_term_frequencies(terms, 5)
    print(search_word_co_occurrences("president", terms, 20))
