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
from myfunctions import getStopWordList,featureExtraction,get_word_features,get_words_in_tweets,getFeatureVector

#initialize stopWords

 

tweets = featureExtraction('trainingandtestdata/training.1600000.processed.noemoticon.csv')
#print (tweets2)
#tweets - format is sentiment and the tweet.

def extract_features(tweet):
    settweet = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in settweet)
    return features

wordlist,word_features = get_word_features(get_words_in_tweets(tweets[:1800])) #my list of many words 
print(wordlist)

#wordlist - words and their frequencies.
#word_features - only words.

#Here I am creating my Training set. 
#I extract feature vector for all tweets in one shot

training_set = nltk.classify.apply_features(extract_features, tweets[:1800])
test_set = nltk.classify.apply_features(extract_features, tweets[1800:])

#****** Naive Bayes Classifier******************************************

classifier = nltk.NaiveBayesClassifier.train(training_set)

# Accuracy
accuracy = nltk.classify.accuracy(classifier, training_set) 

#Printing the accuracy
print (accuracy )

total = accuracy * 100 
print('Naive Bayes Accuracy: %4.2f' % total )

# Accuracy Test Set
accuracyTestSet = nltk.classify.accuracy(classifier, test_set) 

totalTest = accuracyTestSet * 100 
print ('\nNaive Bayes Accuracy with the Test Set: %4.2f' % totalTest )

print ('\nInformative features')
print (classifier.show_most_informative_features(n=15))
#**************************

os.system('mkdir pickled_algos')
classify_buffer = open("pickled_algos/classifier.pickle", 'wb') # store the trained classifier which we can use
                                                                # again and again
pickle.dump(classifier, classify_buffer)
pickle.dump(wordlist,classify_buffer)
classify_buffer.close()


SVC_Classifier = SklearnClassifier(SVC(probability=True))
SVC_Classifier.train(training_set)
print("SVC_Classifier accuracy:", nltk.classify.accuracy(SVC_Classifier, test_set) * 100, "%")

classify_buffer = open("pickled_algos/SVC_Classifier.pickle","wb") # store the trained SVM classifier
pickle.dump(SVC_Classifier, classify_buffer)
classify_buffer.close()

#p,n=analyzeTweets()


   
