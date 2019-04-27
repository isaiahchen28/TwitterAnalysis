# TwitterAnalysis
This project focuses on using data mining and machine learning methods to collect and analyze Tweets that are posted on Twitter. This program uses Twitter's streaming API to collect Tweets that are posted in real time for a desired keyword or query. With the collected data, the program can return term frequencies, term co-occurrences, and perform basic sentiment analysis. The framework for this program is based on example code written by [Marco Bonzanini](https://github.com/bonzanini) and the methodology for sentiment analysis is taken from [Peter D. Turney's paper](https://www.aclweb.org/anthology/P02-1053.pdf) on unsupervised classification based on semantic orientation.

## Setup and Required Modules
Python 3.7 is required, as well as a couple of external modules that can be easily installed:
1. [Tweepy](https://www.tweepy.org) is used for accessing Twitter's Streaming API for data collection.
2. [Natural Language Toolkit](https://www.nltk.org) is used for processing language data.

Also, a config.py file containing API keys and tokens is needed to access Twitter's streaming API. These keys can be provided by the author of the program or any user can [create a Twitter Developer account and use an app to generate API keys and tokens](https://developer.twitter.com/en.html). The config.py file must be formatted as such:
```
consumer_key = "Insert consumer API key here"
consumer_secret = "Insert consumer API secret key here"
access_token = "Insert access token here"
access_secret = "Insert access token secret here"
```

## Data Collection
The first step is to collect data from Twitter in real time. Twitter's streaming API and the Tweepy module are used to accomplish this, and the result will be a .json file containing all the Tweets posted to Twitter that contain a user-specified query or keyword. To start the data collection process, run the following command in your terminal:
```
python collect_data.py -q query -d data -t hh:mm:ss
```
where ```query``` is the keyword of interest, ```data``` is the name of the directory where the .json file will be saved, and ```hh:mm:ss``` is the time duration of the data collection. The query must be either a single word or multiple words within quotation marks. When streaming, the program will timeout after 10 seconds of inactivity if there are no more Tweets containing your query. Also, the config.py file containing acceptable API keys and tokens must be in the same directory as the collect_data.py file.

## Data Analysis
The analysis.py file contains several functions that are used to analyze the collected data:

**Calculate Term Frequencies**
	This function will return the most commonly used terms that appear in the data.
