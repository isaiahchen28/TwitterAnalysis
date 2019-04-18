import tweepy
from tweepy import OAuthHandler

def print_timeline
for status in tweepy.Cursor(api.home_timeline).items(10):
        # Process a single status
        print(status.text)
        print("\n")

def main():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)


if __name__ == '__main__':
    main()
