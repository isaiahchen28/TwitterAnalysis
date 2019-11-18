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
import os
import sys
import numpy as np
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
        count: *int*
            The number of lines in the .json file.
    '''
    # Define list of common characters used for punctuation
    punctuation = list(string.punctuation)
    # Define list of stop-words, which are common words that do not carry
    # significance (conjunctions, adverbs, etc.)
    stop = stopwords.words('english') + punctuation + \
        ["rt", "via", "…", "’", "“", "”", "‘", "1",
            "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    terms = []
    # Open the file
    count = 0
    with open(filename, 'rb') as f:
        # Parse through each line/Tweet in the .json file
        for line in f:
            count += 1
            tweet = json.loads(line)
            # Pre-process the information in the Tweet
            try:
                ppterms = preprocess(tweet["text"])
            except KeyError:
                continue
            # raise Exception("DEBUG")
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
    return terms, count


def calculate_term_frequencies(term_list, n):
    '''
    Calculates term frequencies and will return the most common terms that
    appear in the data.

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
    '''
    Generates the co-occurrence matrix (com), which keeps track of where terms
    appear in the same Tweet. The matrix is built such that the element at
    com[x][y] will be equal to the number of times term x appears in the same
    Tweet as term y. Because this matrix will be symmetric, we only need to
    build a triangular matrix to keep track of all the different times terms
    appear next to each other in Tweets.
    '''
    # Initialize dict subclass for the co-occurrence matrix
    com = defaultdict(lambda: defaultdict(int))
    for tweet in term_list:
        # Build co-occurrence matrix
        for i in range(len(tweet) - 1):
            # Have this loop start from i + 1 to build a triangular matrix
            for j in range(i + 1, len(tweet)):
                # Use sorted function to preserve alphabetical order
                w1, w2 = sorted([tweet[i], tweet[j]])
                if w1 != w2:
                    com[w1][w2] += 1
    return com


def co_occurrent_terms(com, n):
    '''
    Calculate the most frequent co-occurrent terms that appear in the data.

    **Parameters**

        com: *collections.defaultdict*
            The co-occurence matrix generated by the appropriate function.
        n: *int*
            The number of pairs of terms to be returned.

    **Returns**

        terms_max: *list, tuple*
            The list of n pairs of terms that appear together in same Tweet
            the most frequent, along with the number of times they appear
            together.
    '''
    com_max = []
    for t1 in com:
        # For each term in the co-occurrence matrix, sort according to
        # frequency
        t1_max_terms = sorted(
            com[t1].items(), key=itemgetter(1), reverse=True)[:n]
        for t2, count in t1_max_terms:
            # Add each pairing to com_max
            com_max.append(((t1, t2), count))
    # Sort the output list by frequency
    terms_max = sorted(com_max, key=itemgetter(1), reverse=True)
    return terms_max[:n]


def search_word_co_occurrences(keyword, term_list, n):
    '''
    Calculate term co-occurrences for a given keyword.

    **Parameters**

        keyword: *str*
            The word we want to calculate co-occurences for.
        term_list: *list, str*
            A list with all of the individual terms that appear in the .json
            file.
        n: *int*
            The number of terms to return in the list of co-occurrences.

    **Returns**

        count_search_most_common: *list, tuple*
            A list with the words that appear the most frequently along with
            the specified keyword.
    '''
    count_search = Counter()
    for tweet in term_list:
        if keyword in tweet:
            count_search.update(tweet)
    return count_search.most_common(n)


def define_lexicon(filename):
    '''
    Parse through a user-defined lexicon (in a text file) to create a list of
    terms.
    '''
    raw_string_of_file = open(filename, encoding="ISO-8859-1")
    words = []
    for line in raw_string_of_file:
        temp = line.splitlines()[0]
        words.append(temp)
    return words


def sentiment_analysis(term_list, term_counts, com, positive_vocab,
                       negative_vocab, num):
    '''
    Perform sentiment anlysis for a given data set of Tweets.

    **Parameters**

        term_list: *list, str*
            A list with all of the individual terms that appear in the .json
            file.
        term_counts: *collections.Counter*
            A Counter object that is used to keep count of how many times each
            term appears in the term list.
        com: *collections.defaultdict*
            The co-occurence matrix generated by the appropriate function.
        positive_vocab: *list, str*
            The lexicon of words that have a positive connotation.
        negative_vocab: *list, str*
            The lexicon of words that have a negative connotation.
        num: *int*
            The number of words to be returned in the top_pos and top_neg
            lists.

    **Returns**

        semantic_sorted: *list, tuple*
            The sorted list of semantic orientations for all of the terms in
            the term list.
        top_pos: *list, tuple*
            The terms with the highest semantic orienations.
        top_neg: *list, tuple*
            The terms with the lowest semantic orientations.
    '''
    # Calculate the probability of observing term t1 and the probability of
    # observing t1 and t2 together in the same Tweet
    pt = {}
    ptcom = defaultdict(lambda: defaultdict(int))
    ntweets = len(term_list)
    for t1, n in term_counts.items():
        pt[t1] = n / ntweets
        for t2 in com[t1]:
            ptcom[t1][t2] = com[t1][t2] / ntweets
    # Calculate the PMI for each pair of terms
    pmi = defaultdict(lambda: defaultdict(int))
    for t1 in pt:
        for t2 in com[t1]:
            pmi[t1][t2] = log2(ptcom[t1][t2] / (pt[t1] * pt[t2]))
    # Calculate the semantic orientation for every term
    semantic_orientation = {}
    for term, n in pt.items():
        positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
        negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
        semantic_orientation[term] = positive_assoc - negative_assoc
    # Sort the list of semantic orientations
    semantic_sorted = sorted(semantic_orientation.items(),
                             key=itemgetter(1),
                             reverse=True)
    # Define the ten most positive and negative terms that appear in all of
    # the Tweets
    top_pos = semantic_sorted[:num]
    top_neg = semantic_sorted[-num:]
    return semantic_sorted, top_pos, top_neg


def main():
    # Input the filename
    filename = input("Please input the filename of the data to be analyzed: ")
    directory = "data"
    files = os.listdir(directory)
    while True:
        # Check that the file exists
        if ".json" not in filename:
            filename = filename + ".json"
        if filename in files:
            print("Data found. ")
            break
        else:
            filename = input(
                "Data file not found. Please input proper filename or type QUIT to exit. ")
        if filename == "QUIT":
            sys.exit()
    filename = directory + "/" + filename
    # Specify the term filter to be used
    term_filter = "terms_only"
    # Specify the number of terms to be returned from the functions
    n = 10
    # Define the lexicons to be used for sentiment analysis
    positive_vocab = define_lexicon("term_database/positive_words.txt")
    negative_vocab = define_lexicon("term_database/negative_words.txt")
    # Word to be searched
    search_word_ans = input(
        "Do you want to calculate co-occurrences for another search word? (y/n) ")
    while True:
        if search_word_ans == "y":
            SEARCH_WORD = True
            search_word = input(
                "Please input the word to be searched for along side the original query: ")
            break
        elif search_word_ans == "n":
            SEARCH_WORD = False
            break
        else:
            search_word_ans = input("Please enter y/n ")
    # Call upon the functions to perform sentiment analysis
    term_list, num_tweets = generate_term_list(filename, term_filter)
    term_count, term_freq = calculate_term_frequencies(term_list, n)
    com = generate_co_matrix(term_list)
    co_terms = co_occurrent_terms(com, n)
    if SEARCH_WORD:
        searched_word = search_word_co_occurrences(search_word, term_list, n)
    so, top_pos, top_neg = sentiment_analysis(
        term_list, term_count, com, positive_vocab, negative_vocab, n)
    # Print results
    print("Most frequent terms:")
    for i in term_freq:
        print(i)
    print("\nMost frequent co-occurrent terms:")
    for i in co_terms:
        print(i)
    if SEARCH_WORD:
        print("\nFor the word %s, the most frequent co-occurrent terms are:" % search_word)
        for i in searched_word:
            print(i)
    print("\nThe most positive terms:")
    for i in top_pos:
        print(i)
    print("\nThe most negative terms:")
    for i in top_neg:
        print(i)
    # Compute average semantic orientation
    orientations = []
    for i in so:
        orientations.append(i[1])
    print("For a collection of " + str(num_tweets) +
          " tweets, the average semantic orientation is " + str(np.mean(orientations)))


if __name__ == '__main__':
    main()
