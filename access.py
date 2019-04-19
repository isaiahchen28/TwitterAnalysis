"""
This Python script is used to access Twitter and contains some basic
functions.
"""
import config
import tweepy
import json


def print_tweets(api, n):
    """
    This function prints the first n tweets that appear on your home timeline.

    **Parameters**

        api: *class*
            The API class that allows us to access our tweets.
        n: *int*
            The number of tweets to be printed.

    **Returns**

        None
    """
    for status in tweepy.Cursor(api.home_timeline).items(n):
        print(status.text + "\n")


def process_or_store(tweet):
    """
    This function is used to process or store the JSON response from the
    Twitter API.
    """
    print(json.dumps(tweet))


def json_home_timeline(api, n):
    """
    This function processes or stores the JSON response for the first n tweets
    that appear on your home timeline.

    **Parameters**

        api: *class*
            The API class that allows us to access our tweets.
        n: *int*
            The number of tweets to be printed.

    **Returns**

        None
    """
    for status in tweepy.Cursor(api.home_timeline).items(n):
        process_or_store(status.text)


def json_followers(api):
    """
    This function processes or stores the JSON response for all of our
    followers.
    """
    for friend in tweepy.Cursor(api.friends).items():
        process_or_store(friend._json)


def json_tweets(api):
    """
    This function processes or stores the JSON response for all of our
    tweets that we have made.
    """
    for tweet in tweepy.Cursor(api.user_timeline).items():
        process_or_store(tweet._json)


def main():
    # Retrieve API keys and tokens for the app
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_secret = config.access_secret
    # Use OAuth interface to authorize the app to access Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    # Test functions
    print_tweets(api, 10)
    json_home_timeline(api, 10)
    json_followers(api)
    json_tweets(api)


if __name__ == '__main__':
    main()
