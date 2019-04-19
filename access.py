"""
This Python script is used to access Twitter.
"""
import config
import tweepy


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
    # Print the first 10 tweets that appear on my timeline
    for status in tweepy.Cursor(api.home_timeline).items(10):
        # Process a single status
        print(status.text)
        print("\n")


if __name__ == '__main__':
    main()
