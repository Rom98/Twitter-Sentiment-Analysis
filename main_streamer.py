from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import time
import pandas as pd
import re
import csv

#We authenticate ourselves as having a twitter app
#Variables that contains the user credentials to access Twitter API 

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def writeToCsV(document):
    with open('modi.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([document])
    f.close()
    


def myfilter(tweet):
    textTwitter = tweet
    print("##################################")
    print(textTwitter)
    print("##################################")
    #Convert into lowercase
    Tweet = textTwitter.lower()
    Tweet = Tweet.strip()
    
    #Convert www.* or https?://* to URL ie replaces www ot https text with "URL" keyword
    Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',Tweet)
    #Convert @username to User
    Tweet = re.sub('@[^\s]+','TWITTER_USER',Tweet)
    #Remove additional white spac
    Tweet = re.sub('[\s]+', ' ', Tweet)
    Tweet = re.sub("\'", '', Tweet)
    #Replace #word with word Handling hashtags
    Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)
    #trim
    Tweet = Tweet.strip('\'"')
    #Deleting happy and sad face emoticon from the tweet 
    deletelist=[":)",":(","TWITTER_USER","rt","RT","URL","♂️","😂"]
    for i in deletelist:
        Tweet = Tweet.replace(i,'')
    Tweet = re.sub("[^a-zA-Z1-9]+",' ',Tweet)
    return Tweet


#We begin searching our query
#Put your search term
searchquery = ["modi","narendramodi"]

users =tweepy.Cursor(api.search,q=searchquery).items()
count = 0
start = 0
errorCount=0

#We will be storing our data in file called: happy.json
#file = open('test.json', 'wb') 

#here we tell the program how fast to search 
waitquery = 100      #this is the number of searches it will do before resting
waittime = 2.0          # this is the length of time we tell our program to rest
total_number = 2000     #this is the total number of queries we want
justincase = 1         #this is the number of minutes to wait just in case twitter throttles us



text = [0] * total_number
secondcount = 0
 #1 is happy; 2 is sad; 3 is angry; 4 is fearful
#Below is where the magic happens and the queries are being made according to our desires above
while secondcount < total_number:
    try:
        user = next(users)
        count += 1
        
        #We say that after every 100 searches wait 5 seconds
        if (count%waitquery == 0):
            time.sleep(waittime)
            #break

    except tweepy.TweepError:
        #catches TweepError when rate limiting occurs, sleeps, then restarts.
        #nominally 15 minnutes, make a bit longer to avoid attention.
        print( "sleeping....")
        time.sleep(60*justincase)
        user = next(users)
        
        
    except StopIteration:
        break
    try:
        #print "Writing to JSON tweet number:"+str(count)
        text_value = user._json['text']
        language = user._json['lang']
        #print(text_value)
        print(language)
        
        if "RT" not in text_value:
            if language == "en":
                text_value=myfilter(text_value)
                print(text_value)
                text[secondcount] = text_value
                secondcount = secondcount + 1
                print("current saved is:")
                print(secondcount)
                writeToCsV(text_value)

    except UnicodeEncodeError:
        errorCount += 1
        print ("UnicodeEncodeError,errorCount ="+str(errorCount))

'''
print("Creating dataframe:")

d = {"text": text}
df = pd.DataFrame(data = d)

df.to_csv('trump.csv', header=True, index=False, encoding='utf-8')

print ("completed")'''

