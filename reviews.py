import yelp
import argparse
import json
import pprint
import requests
import sys
import urllib

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



def addTrainingBusiness(bizId,rating):
    root = yelp.get_reviews(yelp.API_KEY,bizId)

    

    reviews = root['reviews']
    for r in reviews:
        docs.append(tokenize(r['text']))
        ratings.append(1 if rating > 3 else 0)


    print('added',bizId);

    

def predictBusiness(bizId):
    root = yelp.get_reviews(yelp.API_KEY,bizId)
    reviews = root['reviews']

    predictDocs = []

    for r in reviews:
        predictDocs.append(tokenize(r['text']))

    tfidfMatrix = tfidf(predictDocs,False);

    print(bizSVM.predict(tfidfMatrix))
    
    # print(tfidfMatrix)
    # print(tokens)

    # return vote > 0
    return 1

bizSVM = svm.SVC()

def finishTrainingBusinesses():
    print('training...')
    tfidfMatrix = tfidf(docs);
    
    bizSVM.fit(tfidfMatrix, ratings)

addTrainingBusiness("bPcqucuuClxYrIM8xWoArg",5)
addTrainingBusiness("sZsJooAzpKqOvDysphkqpQ",5)
addTrainingBusiness("cKgUCzMGuRgkbKXUsgeXUw",5)
addTrainingBusiness("yX0pOWG_Be9TjGnm0aihVA",5)
addTrainingBusiness("BCknXEeT9vXQzKGHotsJKQ",3)
addTrainingBusiness("jC3TqY8iKDlIG3hPREBsFA",3)
addTrainingBusiness("Dcpl3tijmPwSnLdYVtqWag",2)
addTrainingBusiness("ZbnFrow_TRDhpzkzTWAVPg",1)
addTrainingBusiness("L-Yj3Y1bYKTSg4uE9KTVBw",4)
addTrainingBusiness("oAq3-dXyDT3k4Mluc1ftTA",4)
addTrainingBusiness("sGAbBm8eX6DY5R5S2NSy6g",3)
addTrainingBusiness("i--dxuKd_6Dx7mwgQ5nl-g",3)
addTrainingBusiness("9n8jDTvkOjoH3fD_Y9KC1g",2)
addTrainingBusiness("NzmJJvTEotNCEduQUcIwBg",2)
addTrainingBusiness("1XCR1GxL44O2hg3ehRwtMA",4)
addTrainingBusiness("d7xjodUIGqFYexZoXEiF4Q",3)
addTrainingBusiness("gtfLQysuCBEAQk3wwWxwTg",4)
addTrainingBusiness("Dv0OHpQSL4hOGl2KAEVvlA",3)
addTrainingBusiness("HkHTdTvzbn-bmeQv_-2u0Q",3)
addTrainingBusiness("nJBwEYaulNXHPAUP0OBRtg",3)
addTrainingBusiness("-av1lZI1JDY_RZN2eTMnWg",2)
addTrainingBusiness("eEKfOX6KtQmLgb8z-1VfUA",3)
addTrainingBusiness("qjLlFfu2pnJ9lVYlj-4QVg",3)
addTrainingBusiness("DLw9rK8Qb6l7ESgxtR47qQ",4)
addTrainingBusiness("Gt4z3AylNTsEPDkzkaC7HA",3)
addTrainingBusiness("-av1lZI1JDY_RZN2eTMnWg",3)
addTrainingBusiness("JUI0-5ENNGAoqSF8v1LO8Q",5)
addTrainingBusiness("HhVmDybpU7L50Kb5A0jXTg",5)
addTrainingBusiness("zLC9OtK3SKAW_g6SXijr4w",5)

addTrainingBusiness("7usumJrTK_qs2GbSd8zIvg",4)
addTrainingBusiness("iAuOpYDfOTuzQ6OPpEiGwA",3)
addTrainingBusiness("mxMwo3zfJwVoCIayeNcA5w",3)
addTrainingBusiness("DkZuVzYuylBanEsWK7mNGw",4)
addTrainingBusiness("NblDoJBEwhkJyvAuxzh4rg",4)
addTrainingBusiness("qqs7LP4TXAoOrSlaKRfz3A",3)
addTrainingBusiness("3aKmNE2coy5YLBCIu676og",4)
addTrainingBusiness("1JF9TbJ2d5hH8xsQvvklHg",4)
addTrainingBusiness("w_7VFr4bZiTl65HWEf0SVQ",3)
addTrainingBusiness("5T0h9YCsXiDZyBsVIN9gcg",4)
addTrainingBusiness("DkZuVzYuylBanEsWK7mNGw",5)
addTrainingBusiness("e9Dem4OvxH2blvEbMule3g",3)
addTrainingBusiness("rabwxNMs47smKp54CE3e8w",2)
addTrainingBusiness("N3J76CRP2H52NUo4VFuS3A",4)
addTrainingBusiness("bPcqucuuClxYrIM8xWoArg",4)
addTrainingBusiness("qqs7LP4TXAoOrSlaKRfz3A",5)
addTrainingBusiness("7wHLFohwCw8l6WS-feLjeg",5)
addTrainingBusiness("V3-Bbq9uH6BnM2XsFXl6Sg",3)
addTrainingBusiness("8nNB_yG1gzVpbqNH2EBucg",5)
addTrainingBusiness("8BBcTUOmXT0dJ33hYtLUAw",5)
addTrainingBusiness("lxpGgLcJAGAlbaC1PnJ0xQ",4)
addTrainingBusiness("Ndd8IYE_9rTrwHygA5AMwQ",5)
addTrainingBusiness("QDF7w0casJ78PcPmtMDISw",5)
addTrainingBusiness("Vg1C_1eqwIwkZLIXGMTW3g",5)
addTrainingBusiness("2px99IppAcnxR238eq_8_w",5)
addTrainingBusiness("ckQdUPdUOX18yOhE2aV8sA",5)
addTrainingBusiness("MNwJ-40jcDZakqEQP4bk4g",4)
addTrainingBusiness("kByQQ4yd7ZbA0MAQKmRVvg",2)
addTrainingBusiness("I3STZd5iAvUL9MNLF_DUug",4)
addTrainingBusiness("aMF8cG445ONPRKBsBYqofg",4)
addTrainingBusiness("wdOOK3K6vzQy1d_OIk-U9w",1)
addTrainingBusiness("hXY9Yq0nOLgHsWLbjam--A",2)
addTrainingBusiness("2qIZlW8YSLL8a7I6KkJdHQ",4)
addTrainingBusiness("hHtmzOwkdNj93QnKaUr5og",1)
addTrainingBusiness("qIYoTx7pTNsGjAFXp9noTg",1)
addTrainingBusiness("o_TPuqXuH-O_FbEkFNACUA",5)
addTrainingBusiness("SnMUTGhY2nW2Ldb0QJAjAg",4)
addTrainingBusiness("rbcfYmJtqwIkk17IeOI5Kw",5)
addTrainingBusiness("xVEtGucSRLk5pxxN0t4i6g",5)
addTrainingBusiness("DaxEPd4fQNCksMy3xzBraA",2)
addTrainingBusiness("vsFFbN71ehRCp46KeR5RdQ",5)
addTrainingBusiness("WzrMNz9eUF78RgZGDTS8xg",4)
addTrainingBusiness("NxjUiGBNgyDErKXnmQ3s3w",5)
addTrainingBusiness("5T0h9YCsXiDZyBsVIN9gcg",5)
addTrainingBusiness("Vg1C_1eqwIwkZLIXGMTW3g",4)

finishTrainingBusinesses();

predictBusiness("TEaBolNAkOdRm2gvIYz4OQ")
predictBusiness("Lqp3uwGJU6CHyys-eerMmQ")
predictBusiness("qzjMO-bLXirGU1Q4_8vJEg")



def main():
    pass;



if __name__ == '__main__':
    main()