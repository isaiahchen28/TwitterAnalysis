"""
This Python script is used to access Twitter and contains some basic functions
for collecting data. To properly run this script, enter the following command
in the terminal:

python collect_data.py -q QUERY -d data -t hh:mm:ss

where QUERY is the query of interest, data is the directory where the json
file will be saved to, and time is the time that the stream will run for. If
the query does not appear in enough tweets after 5 seconds, the stream will
time out and return an error.
"""
import argparse
import string
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import config


def get_parser():
    """
    Get the parser for any arguments in the command line.
    """
    parser = argparse.ArgumentParser(description="Download Tweets")
    # Add argument for the query
    parser.add_argument("-q", "--query", dest="query",
                        help="The desired keyword", default='-')
    # Add argument for the directory for the file to be saved
    parser.add_argument("-d", "--data-dir", dest="data_dir",
                        help="The directory where the data will be saved in a .json file")
    parser.add_argument("-t", "--time-limit", dest="time_limit",
                        help="The desired amount of time to run the stream. Format should be hh:mm:ss")
    return parser


def get_sec(time_str):
    """
    Converts time string (hh:mm:ss) into seconds.
    """
    h, m, s = time_str.split(':')
    return float(int(h) * 3600 + int(m) * 60 + int(s))


def convert_valid(char):
    """
    Converts a character into an appropriate one for use in filenames. If a
    character is invalid, it will be replaced with a '_' character.
    """
    # Define string with all valid characters for filenames
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    # Check if the character is valid or not and replace the invalid character
    if char in valid_chars:
        return char
    else:
        return '_'


def format_filename(filename):
    """
    Converts the filename into a string with suitable characters. It takes in
    the name of the file to be converted and will return the appropriate
    string.
    """
    return ''.join(convert_valid(char) for char in filename)


class MyListener(StreamListener):
    """
    StreamListener object that is used to stream data from Twitter.

    **Parameters**

        data_dir: *str*
            The name of the directory where the data will be stored.
        query: *str*
            The keyword of interest.
        time_limit: *int*
            The time limit for the stream to run
    """

    def __init__(self, data_dir, query, time_limit):
        # Make sure the filename is formatted properly
        query_filename = format_filename(query)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_filename)
        self.start_time = time.time()
        self.time_limit = time_limit

    def on_data(self, data):
        """
        Write an individual Tweet to the output file. The data input is
        encoded as a unicode type.
        """
        # Check if the time limit has been reached
        if (time.time() - self.start_time) < self.time_limit:
            try:
                # Write data to the output file and print it to the terminal
                with open(self.outfile, 'a') as f:
                    f.write(data)
                    print(data)
                    return True
            # Error handling
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                time.sleep(5)
            return True
        else:
            print("Time limit has been reached.")
            return False

    def on_error(self, status):
        """
        Print the error status in case an error occurs.
        """
        print(status)
        return True


def main():
    # Define parser and retrieve the input arguments
    parser = get_parser()
    args = parser.parse_args()
    # Retrieve API keys and tokens
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_secret = config.access_secret
    # Authenticate user
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # Stream Twitter data using StreamListener object
    twitter_stream = Stream(auth, MyListener(
        args.data_dir, args.query, get_sec(args.time_limit)), timeout=5)
    twitter_stream.filter(track=[args.query])


if __name__ == '__main__':
    main()
