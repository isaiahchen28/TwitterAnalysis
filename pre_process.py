"""
This Python script contains functions that are used to pre-process the data
stored in .json files.
"""
import re


def tokenize(s):
    """
    Split a string of text into individual tokens.

    **Parameters**

        s: *str*
            The text to be split into separate strings.

    **Returns**

        tokens: *list, str*
            A list of the individual tokens.
    """
    # Define string of various emoticons to be recognized as tokens
    emoticons_str = r"""
    (?:
        [:=;]
        [oO\-]?
        [D\)\]\(\]/\\OpP]
    )"""
    # Define regular expressions which contain possible patterns for text in
    # Tweets, such as hashtags, URLs, and numbers
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
    # Use Verbose and Ignorecase flags to ignore spaces in original strings
    # and read both lowercase and uppercase characters
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')',
                           re.VERBOSE | re.IGNORECASE)
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    """
    Call the tokenize function above and also handle emoticons properly.

    **Parameters**

        s: *str*
            The text to be split into separate strings.
        lowercase: *boolean*
            A flag to decide whether the tokens will contain any uppercase
            characters or not. If lowercase is True, then all uppercase
            characters will be converted to lowercase, except for emoticons. 

    **Returns**

        
    """
    emoticons_str = r"""
    (?:
        [:=;]
        [oO\-]?
        [D\)\]\(\]/\\OpP]
    )"""
    emoticon_re = re.compile(r'^'+emoticons_str+'$',
                             re.VERBOSE | re.IGNORECASE)
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]
    return tokens


tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(preprocess(tweet))
