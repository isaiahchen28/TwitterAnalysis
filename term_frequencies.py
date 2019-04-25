"""
This Python script is used to analyze term frequencies.
"""
import string
from nltk import bigrams
from nltk.corpus import stopwords
from collections import Counter
import json
import pre_process


def calculate_term_frequencies(filename, term_filter, n):
    """
    Observe which terms appear the most in a given Twitter dataset.

    **Parameters**

        filename: *str*
            The name/location of the .json file with the Twitter dataset.
        term_filter: *str*
            The specified filter to be used for terms. Possible filters
            include:
                "default" - considers all terms
                "remove_stop_words" - does not consider stop-words
                "single_terms" - only counts terms once
                "hashtags" - only counts hashtags
                "terms_only" - only counts terms (no hashtags or mentions)
                "bigrams" - only counts bigrams
        n: *int*
            The number of arguments to be returned.

    **Returns**

        common_terms: *list, tuples*
            A list of tuples containing the most common terms and the number
            of times they occur.
    """
    # Define list of common characters used for punctuation
    punctuation = list(string.punctuation)
    # Define list of stop-words, which are common words that do not carry
    # significance (conjunctions, adverbs, etc.)
    stop = stopwords.words('english') + punctuation + ["rt", "via"]
    # Open the file
    with open(filename, 'r') as f:
        # Initialize counter class to access useful methods
        count_all = Counter()
        # Parse through each line/Tweet in the .json file
        for line in f:
            tweet = json.loads(line)
            # Pre-process the information in the Tweet
            ppterms = pre_process.preprocess(tweet['text'])
            # Apply the appropriate filter as specified by the user
            if term_filter == "remove_stop_words":
                terms = [term for term in ppterms if term not in stop]
            elif term_filter == "hashtags":
                terms = [term for term in ppterms if term.startswith('#')]
            elif term_filter == "terms_only":
                terms = [term for term in ppterms if term not in stop and not term.startswith(('#', '@'))]
            elif term_filter == "bigrams":
                temp = [term for term in ppterms if term not in stop]
                terms = bigrams(temp)
            elif term_filter == "single_terms":
                temp = [term for term in ppterms]
                terms = set(temp)
            elif term_filter == "default":
                terms = [term for term in ppterms]
            else:
                raise Exception("Invalid term filter.")
            # Update the counter
            count_all.update(terms)
        common_terms = count_all.most_common(n)
    return common_terms

if __name__ == '__main__':
    filename = "data/stream_avengers.json"
    term_filter = "bigrams"
    print(calculate_term_frequencies(filename, term_filter, n=10))
