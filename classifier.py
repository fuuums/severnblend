# outputs if the tweet is a positive (1) or negative (-1) sentiment.
# put it in a loop if u want it to be continuous
# make sure twats/labels file is in the same directory

from collections import Counter
import csv
import re
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# start replaceTwoOrMore
def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

# start process_tweet
def processTweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub('\$[a-z]+',"COMPANY",tweet)
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub('\$[0-9]+', "MONTEY", tweet)
    tweet = re.sub('[0-9]+', "NUMBER", tweet)
    tweet = re.sub('\x92','',tweet) #weird ? char gone
    tweet = tweet.strip('\'"')
    return tweet

if __name__ == '__main__':
    # load data
    with open('twats') as f1:
        twats = f1.read().splitlines()
    with open('labels') as f2:
        labels = f2.read().splitlines()
    slabel = map(int, labels)
    ulabel = map(int, labels)
    plabel = map(int, labels)

    #### change this to get input from wherever, put it in the list
    l      = ['sell sell sell']

    for i in range(len(slabel)):
        if slabel[i] is not 2:
            slabel[i] = 0
    for i in range(len(ulabel)):
        if ulabel[i] is not 0:
            ulabel[i] = 1
    for i in range(len(plabel)):
        if plabel[i] is not 1:
            plabel[i] = -1

    # cleanse tweets
    for i in range(len(twats)):
        twats[i] = processTweet(twats[i])

    # tokenize text
    count_vect = CountVectorizer()
    x_train_counts = count_vect.fit_transform(twats)

    # frequencies
    tf_transformer = TfidfTransformer(use_idf=False).fit(x_train_counts)
    x_train_tf = tf_transformer.transform(x_train_counts)

    # train classifiers
    spam = MultinomialNB().fit(x_train_tf, slabel)

    # prepare incoming tweet for analysis
    xnc = count_vect.transform(l)
    xnt = tf_transformer.transform(xnc)
    pdt = spam.predict(xnt)

    #if pdt[0] == 2:
         # spam exit condition
        
    usfl = MultinomialNB().fit(x_train_tf, ulabel)
    pdt = usfl.predict(xnt)

    #if pdt[0] == 0:
         # not useful exit condition
        
    psng = MultinomialNB().fit(x_train_tf, plabel)
    pdt = psng.predict(xnt)
    
    print pdt[0]
