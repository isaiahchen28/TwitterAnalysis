"""
This Python script contains functions that are used to pre-process the data
stored in .json files.
"""
import re


def tokenize(s):
    """
    Split a string of text into individual tokens

    **Parameters**

        s: *str*
            The text to be split into separate strings.

    **Returns**

        
    """
    emoticons_str = r"""
    (?:
        [:=;]
        [oO\-]?
        [D\)\]\(\]/\\OpP]
    )"""
    regex_str = [
        emoticons_str,
        r"<[^>]+>",
        r"(?:@[\w_]+)",
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
        r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+",
        r"(?:(?:\d+,?)+(?:\.?\d+)?)",
        r"(?:[a-z][a-z'\-_]+[a-z])",
        r"(?:[\w_]+)",
        r"(?:\S)"]
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    emoticons_str = r"""
    (?:
        [:=;]
        [oO\-]?
        [D\)\]\(\]/\\OpP]
    )"""
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]
    return tokens

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(preprocess(tweet))