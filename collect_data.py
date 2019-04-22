"""
This Python script is used to access Twitter and contains some basic functions
for collecting data. To properly run this script, enter the following command
in the terminal:

python collect_data.py -q QUERY -d data

where QUERY is the query of interest and data is the directory where the json
file will be saved to.
"""
import argparse
import config
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import string
import time
import json


def get_parser():
    """
    Get the parser for any arguments in the command line.
    """
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q", "--query", dest="query",
                        help="Query/Filter", default='-')
    parser.add_argument("-d", "--data-dir", dest="data_dir",
                        help="Output/Data Directory")
    return parser


class MyListener(StreamListener):
    """
    StreamListener object that is used to stream data from Twitter.
    """

    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """
    Converts the filename into a string with suitable characters. It takes in
    the name of the file to be converted and will return the appropriate
    string.
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """
    Converts a character into an appropriate one for use in filenames. If a
    character is invalid, it will be replaced with a '_' character.
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


def main():
    parser = get_parser()
    args = parser.parse_args()
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_secret = config.access_secret
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
    twitter_stream.filter(track=[args.query])


if __name__ == '__main__':
    main()
