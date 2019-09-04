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
The analysis.py file contains several functions that are used to analyze the collected data. The important ones are listed below:

**Calculate Term Frequencies:** This function will return the most commonly used terms that appear in the data, along with the number of times each term appears.

**Calculate Term Co-Occurrences:** This function will return the most commonly used pairs of terms that appear in the same Tweets. This gives us a better idea of the context in which certain terms appear.

**Search Word Co-Occurrences:** Given a user-specified keyword, this function will return the terms that appear the most frequently in the same Tweets with the keyword. If we have a specific term or keyword and we want to see which other terms appear alongside it, this function is usefl in this regard.

**Sentiment Analysis:** This function performs sentiment analysis using Semantic Orientation (SO) and Pointwise Mutual Information (PMI) as the relevant metrics. The semantic orientation of a word is defined as the difference between its associations with other positive and negative words. The PMI is an indicator of how associated two terms are. The relevant equations for calculating both of these metrics can be found in Peter D. Turney's paper, which is linked above. This function also makes use of compiled lexicons of positive and negative words that are stored in two appropriately named text files. These lexicons have been compiled by [Minqing Hu and Bing Liu](https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon).

The main function in the analysis.py file can be easily changed to run the appropriate functions. Simply run the python file in the terminal to perform the analysis. Line 272 must have the correct filename for the .json file, line 274 must have the desired term filter (the different filters are described in lines 34-40), and the desired search word can be input on line 281.

## Work in Progress
This code is being continuously improved to add more functionalities. Please contact Isaiah Chen (email: ichen23@jhu.edu) with any questions or concerns.
