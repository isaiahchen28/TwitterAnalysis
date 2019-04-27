"""
This Python script is used to analyze term frequencies.
For each tweet in a .json file, there are different attributes:
    text - the text of the Tweet
    created_at - the date of the creation of the Tweet
    favorite_count - the number of times the Tweet has been favorited
    retweet_count - the number of times the Tweet has been retweeted
    lang - the language that the Tweet is written in
    user - the profile/handle of the Tweet's author
These function will only use the text information in each tweet.
"""
import string
from nltk.corpus import stopwords
import json
import pre_process
from collections import Counter
from collections import defaultdict
from operator import itemgetter
import math


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
                terms.append(list(set(temp)))
            elif term_filter == "single_stop_words":
                temp = [term for term in ppterms if term not in stop]
                terms.append(list(set(temp)))
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
    return count_all, count_all.most_common(n)


def generate_co_matrix(term_list):
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
    return com


def co_occurrent_terms(com, n):
    com_max = []
    for t1 in com:
        t1_max_terms = sorted(
            com[t1].items(), key=itemgetter(1), reverse=True)[:n]
        for t2, count in t1_max_terms:
            com_max.append(((t1, t2), count))
    terms_max = sorted(com_max, key=itemgetter(1), reverse=True)
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


def define_lexicon(filename):
    raw_string_of_file = open(filename, encoding="ISO-8859-1")
    words = []
    for line in raw_string_of_file:
        temp = line.splitlines()[0]
        words.append(temp)
    return words


if __name__ == '__main__':
    filename = "data/stream_brexit.json"
    term_filter = "terms_only"
    term_list = generate_term_list(filename, term_filter)
    term_count, term_freq = calculate_term_frequencies(term_list, 20)
    com = generate_co_matrix(term_list)
    co_terms = co_occurrent_terms(com, 20)
    searched_word = search_word_co_occurrences("fucking", term_list, 20)

    # n_docs is the total n. of tweets
    p_t = {}
    p_t_com = defaultdict(lambda: defaultdict(int))
    n_docs = len(term_list)
    for term, n in term_count.items():
        p_t[term] = n / n_docs
        for t2 in com[term]:
            p_t_com[term][t2] = com[term][t2] / n_docs

    positive_vocab = define_lexicon("positive_words.txt")
    negative_vocab = define_lexicon("negative_words.txt")

    pmi = defaultdict(lambda: defaultdict(int))
    for t1 in p_t:
        for t2 in com[t1]:
            denom = p_t[t1] * p_t[t2]
            pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)

    semantic_orientation = {}
    for term, n in p_t.items():
        positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
        negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
        semantic_orientation[term] = positive_assoc - negative_assoc

    semantic_sorted = sorted(semantic_orientation.items(),
                             key=itemgetter(1),
                             reverse=True)
    top_pos = semantic_sorted[:10]
    top_neg = semantic_sorted[-10:]

    print(top_pos)
    print(top_neg)
