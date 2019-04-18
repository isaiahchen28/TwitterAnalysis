import tweepy
from tweepy import OAuthHandler
from main import twitter

consumer_key = twitter[0]
consumer_secret = twitter[1]
access_token = twitter[2]
access_secret = twitter[3]
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)