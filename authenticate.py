import tweepy
from tweepy import OAuthHandler


def main():
    consumer_key = "OeB3k7xS1OFFinKYHWk7sBCkH"
    consumer_secret = "LY83hw0w5DU8Z4PXnRisq0mv15Pb5QeIHVJomIBUV3yXUbeeNt"
    access_token = "3806144777-QrAPkEJNNwBF04GzJTblYrs6Pmx1FBsoGNmtEIP"
    access_secret = "ctkFe4gddfNUDwSOZubxOg4Ua4uEcQ7eHpXUXavK3l8p8"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    for status in tweepy.Cursor(api.home_timeline).items(10):
    	# Process a single status
    	print(status.text)
        print("\n")


if __name__ == '__main__':
    main()
