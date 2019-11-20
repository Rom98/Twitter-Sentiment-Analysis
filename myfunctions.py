import csv,re
from nltk.corpus import stopwords
import random

import sys ,os
import csv
import tweepy
import re 
import nltk
from nltk.classify import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from nltk.corpus import stopwords
import nltk.classify.util
import random
import pickle
from sklearn.svm import SVC
#starting the function 
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end
 
#starting the function 
def getStopWordList(stopWordListFileName):
#read the stopwords file and build a list
    stopWords = []
    #stopWords.append('TWITTER_USER')
    stopWords.append('URL')
 
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

stopWords = []
stopWords = getStopWordList('StopWords.txt')

def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
 
def featureExtraction(path):
    #Reading training dataset and filtering , extracting features
    inpTweets = csv.reader(open(path, 'rt' ,encoding="utf-8"), delimiter=',', quotechar='|')
    tweets = []
  
    for rowTweet in inpTweets:
        sentiment = rowTweet[0]
        tweet = rowTweet[1]
        featureVector = getFeatureVector(tweet)
        tweets.append((featureVector, sentiment))
    #print "Printing the tweets con su sentiment"
    #print tweets
    random.shuffle(tweets)
    return tweets #Here I am returning the tweets inside the array plus its sentiment
#end

#Classifier 
def get_words_in_tweets(tweets):      # creates a list of only words from the "tweets" list excluding the sentiment
    all_words = []
    for (text, sentiment) in tweets:
        all_words.extend(text)
    return all_words

def get_word_features(wordlist):
    # This line calculates the frequency distrubtion of all words in tweets
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    # This prints out the list of all distinct words in the text in order
    # of their number of occurrences.
    return wordlist,word_features

