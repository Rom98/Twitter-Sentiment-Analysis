#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
from myfunctions import getFeatureVector
import csv
from plot import MyPlots

tweet=input("Enter a sentence\n")

classify_buffer = open(r'pickled_algos/classifier.pickle', 'rb') #NB Classifier
classifier=pickle.load(classify_buffer)
wordlist=pickle.load(classify_buffer)
word_features=wordlist.keys()

classify_buffer = open(r"pickled_algos/SVC_Classifier.pickle", 'rb')#SVM Classifier
SVC_Classifier = pickle.load(classify_buffer)

def extract_features(tweet):
    settweet = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in settweet)
    return features

print("Naive Bayes")
predicted_sentiment=classifier.classify(extract_features(getFeatureVector(tweet)))
ppos=classifier.prob_classify(extract_features(getFeatureVector(tweet))).prob('positive')
print(predicted_sentiment+'\nPositive probablity :'+str(ppos)+'\nNegative Probablity:'+str(1-ppos))

print("\n\nSVM")
predicted_sentiment2=SVC_Classifier.classify(extract_features(getFeatureVector(tweet)))
ppos=SVC_Classifier.prob_classify(extract_features(getFeatureVector(tweet))).prob('positive')
print(predicted_sentiment2+'\nPositive probablity :'+str(ppos)+'\nNegative Probablity:'+str(1-ppos))


def analyzeTweets(choice): #choice = input("svm or naivebayes ?")
    ncnt=0
    pcnt=0
    ppos=0.001
    inpTweets = csv.reader(open('trump.csv', 'rt' ,encoding="utf-8"), delimiter=',', quotechar='|')  
    for rowTweet in inpTweets:
        raw_input=rowTweet[0]
        
        raw_input = raw_input.lower()
        #raw_input = raw_input.split()
        print(raw_input)
        #predicted_sentiment=classifier.classify(extract_features(rowTweet))
        if choice=='naivebayes':
            ppos=classifier.prob_classify(extract_features(getFeatureVector(raw_input))).prob('positive')
        elif choice=='svm':
            ppos=SVC_Classifier.prob_classify(extract_features(getFeatureVector(raw_input))).prob('positive')
        if(ppos<=0.5009):
            ncnt += 1
        else:
            pcnt +=1
    return pcnt,ncnt

def naive_plot():
    pcnt,ncnt=analyzeTweets('naivebayes')
    print(pcnt,ncnt)
    MyPlots.plot([pcnt,ncnt])