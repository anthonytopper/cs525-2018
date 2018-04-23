# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 17:03:43 2018

@author: fzhan
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data=pd.read_csv('CF_data.csv',index_col=0)
data0=pd.read_csv('yelp_business.csv')
data0=data0.iloc[:,[0,12]]
data1=data0[list(map(lambda x: 'Restaurants' in x,data0['categories']))]
data=data.merge(data1,on='business_id').iloc[:,:3]
'''def present(idn,pref):
    d={}
    for i,idn in enumerate(idn):
        d[idn]=pref+str(i)
    return d'''
def present(idn):
    d={}
    for i,idn in enumerate(idn):
        d[idn]=i
    return d
ud=present(data['user_id'])
data['user_id']=list(map(lambda x: ud[x],data['user_id']))
bd=present(data['business_id'])
data['business_id']=list(map(lambda x: bd[x],data['business_id']))

#exploratory analysis
user_num=len(set(data['user_id']))
business_num=len(set(data['business_id']))

business_popu=data.iloc[:,:2].groupby('business_id').count()
business_popu.columns=['review_count']
plt.hist(business_popu.iloc[:,0].tolist(),range=(0,400))
user_popu=data.iloc[:,:2].groupby('user_id').count()
user_popu.columns=['review_count']
plt.hist(user_popu.iloc[:,0].tolist(),range=(0,40))

#user just with less than two reviews as test data
data3=data.set_index('user_id')
testdata=data3[user_popu['review_count']<=2]
traindata=data3[user_popu['review_count']>2]

#split 
from sklearn.model_selection import train_test_split
train,validate=train_test_split(traindata, test_size=0.33,random_state=42,stratify=traindata.index)
'''def transdf(data):
    d=pd.DataFrame(data)
    d['user_id']=data.index
    d.index=range(len(data))
    return d
train_dist=transdf(train.iloc[:,0].groupby(train.index).count())
validate_dist=transdf(validate.iloc[:,0].groupby(validate.index).count())
dist=train_dist.merge(validate_dist,on='user_id',how='outer')
'''
testdata.sort_index().to_csv('testdata.csv')
train.sort_index().to_csv('train.csv')
validate.sort_index().to_csv('validate.csv')

batch_size=500

class convertdata(object): 
    def __init__(self, batch_size):
        train=pd.read_csv('train.csv',index_col=0)
        validate=pd.read_csv('validate.csv',index_col=0)
        
        
        users=sorted(list(set(train.index).union(set(validate.index))))
        nb_users=len(users)
        business=sorted(list(set(train['business_id']).union(set(validate['business_id']))))
        nb_business=len(business)
        dic=present(business)
        # Converting the data into an array with users in lines and movies in columns
    
    def convert(self,data,users,dic,nb_business,batch_size):
        for i,id_users in enumerate(users):
            U=[]
            id_business = data['business_id'][data.index == id_users]
            ind=list(map(lambda x:dic[x],id_business))
            #id_business = list(map(lambda x:business.index(x),l))
            id_ratings = data['stars'][data.index == id_users]
            ratings = np.zeros(nb_business)
            ratings[ind] = id_ratings
            if i%batch_size==0:
                if i!=0:
                    yield np.array(U)
                U=[list(ratings)]
            else:
                U.append(list(ratings))

        
    self.train_set = self.convert(train,users,dic,nb_business,batch_size)
    self.val_set = self.convert(validate,users,dic,nb_business,batch_size)


#def convert(data):
#    data=data.sort_index()
#    data['user_id']=data.index
#    data=data.set_index(['user_id','business_id'])
#    return data.unstack()

#convert(train)
    
    

