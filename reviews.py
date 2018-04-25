import yelp
import argparse
import json
import pprint
import requests
import sys
import urllib
import csv

from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer


try:
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


def tokenize(text):
    import re
    clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
    tokens = clean_string.split()
    return tokens

def tf(term,tokens):
    c = 0;
    for x in tokens:
        if x == term:
            c += 1;
    return c

def idf(term,docs):
    c = 0
    for x in docs:
        if term in x:
            c += 1;

    import math
    return math.log((len(docs)+1)/(c+1))



# docs = array of documents, each one a list of tokens
# returns array of 
def tfidf(docs,add=True):
    results = []

    for x in docs:
        for token in x:
            if add and token not in tokens:
                tokens.append(token)

    for d in docs:
        doc = [0 for _ in range(len(tokens))]
        for i in range(len(tokens)):
            t = tokens[i]
            doc[i] = tf(t,d) * idf(t,docs)

        results.append(doc)

    return results

tokens = []
docs = []
ratings = []

# "Vg1C_1eqwIwkZLIXGMTW3g"



def addTrainingEntry(text,rating):
    docs.append(tokenize(text))
    ratings.append(1 if rating > 3 else 0)

def predictEntry(text):
    predictDocs = [tokenize(text)]
    tfidfMatrix = tfidf(predictDocs,False);
    return bizSVM.predict(tfidfMatrix)

def addTrainingBusiness(bizId,rating):
    root = yelp.get_reviews(yelp.API_KEY,bizId)

    


    if not 'reviews' in root: 
        print(root)
        return

    reviews = root['reviews']
    for r in reviews:
        addTrainingEntry(r['text'],rating)


    print('added',bizId);

    

def predictBusiness(bizId):
    root = yelp.get_reviews(yelp.API_KEY,bizId)
    reviews = root['reviews']

    predictDocs = []

    for r in reviews:
        predictDocs.append(tokenize(r['text']))

    tfidfMatrix = tfidf(predictDocs,False);

    result = bizSVM.predict(tfidfMatrix)
    
    vote = 0

    for i in result:
        vote += 1 if i > 0 else -1

    return 1 if vote > 0 else 0

bizSVM = svm.SVC()

def finishTrainingBusinesses():
    print('training...')
    tfidfMatrix = tfidf(docs);
    
    bizSVM.fit(tfidfMatrix, ratings)




def main():
    with open('train.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        count = 0
        for row in reader:
            if first:
                first = False;
                continue
            count += 1
            if count > 1000:
                break
            addTrainingBusiness(row[1],int(row[2]))

    finishTrainingBusinesses()



    with open('validate.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                first = False;
                continue
            print(predictBusiness(row[1]),'=?',1 if int(row[2]) > 3 else 0);

    pass;



if __name__ == '__main__':
    main()