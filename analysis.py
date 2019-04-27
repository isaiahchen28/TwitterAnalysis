'''
This Python script contains different functions for analyzing data from a
.json file with Tweets. For each tweet in a .json file, there are several
different attributes, such as:
    text - the text of the Tweet
    created_at - the date of the creation of the Tweet
    favorite_count - the number of times the Tweet has been favorited
    retweet_count - the number of times the Tweet has been retweeted
    lang - the language that the Tweet is written in
    user - the profile/handle of the Tweet's author
These functions will only utilize the text information in each tweet.
'''
import string
from nltk.corpus import stopwords
import json
from collections import Counter
from collections import defaultdict
from operator import itemgetter
from math import log2
from pre_process import preprocess


def generate_term_list(filename, term_filter):
    '''
    Generate a list of all the terms that appear in a .json file

    **Parameters**

        filename: *str*
            The name of the .json file to be input.
        term_filter: *str*
            The type of filter to be used for parsing through all the words in
            the Tweets. There are six different filters that can be used:
                default - considers all of the terms
                remove_stop_words - does not consider stop-words
                hashtags - only considers hashtags and no other terms
                terms_only - does not consider hashtags or mentions
                single_terms - only counts terms once in a Tweet
                single_stop_words - only counts terms once and does not
                                    consider stop-words

    **Returns**

        terms: *list, str*
            A list with all of the individual terms that appear in the .json
            file.
    '''
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
            ppterms = preprocess(tweet['text'])
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
    '''
    Calculates term frequencies and will return the most common terms that
    appear in all of the Tweets.

    **Parameters**

        term_list: *list, str*
            A list with all of the individual terms that appear in the .json
            file.
        n: *int*
            The number of terms to return in the list of most common terms.

    **Returns**

        count_all: *collections.Counter*
            A Counter object that is used to keep count of how many times each
            term appears in the term list.
        most_common_terms: *list, tuple*
            A list of the n most common terms that appear in the term list,
            along with the number of times each term appears.
    '''
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
    filename = "data/stream_trump.json"
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
            pmi[t1][t2] = log2(p_t_com[t1][t2] / denom)

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
