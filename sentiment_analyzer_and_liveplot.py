#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time,pickle,csv
import numpy as np

style.use("ggplot")

classify_buffer = open(r'pickled_algos/classifier.pickle', 'rb')
classifier=pickle.load(classify_buffer)
wordlist=pickle.load(classify_buffer)
word_features=wordlist.keys()


fig = plt.figure()
axis = fig.add_subplot(1,1,1)

xar = []
yar = []
x = 0
y = 0

def extract_features(tweet):
    settweet = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in settweet)
    return features

def animate(i):
    xar=[]
    yar=[]
    x=0
    y=0
    data = csv.reader(open('trump.csv', 'rt' ,encoding="utf-8"), delimiter=',', quotechar='|')
    for rowTweet in data:
        raw_input=rowTweet[0]
        raw_input = raw_input.lower()
        raw_input = raw_input.split()
        #predicted_sentiment=classifier.classify(extract_features(rowTweet))
        ppos=classifier.prob_classify(extract_features(raw_input)).prob('positive') #Extrct common words from the tweet 
                                                                    #and calculate it's probability of positive words.
        x += 1
        if(ppos<=0.5):
            y -= 1
        else:
            y += 1
        xar.append(x)
        yar.append(y)

    axis.clear()
    axis.plot(xar,yar)

ani = animation.FuncAnimation(fig, animate, interval=1000)
#plt.show()


plt.show()