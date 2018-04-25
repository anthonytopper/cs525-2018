# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 12:06:01 2018

@author: fzhan
"""

import pandas as pd
import numpy as np
rbm=pd.read_csv('rbmPred.csv',index_col=0)
ae=pd.read_csv('aePred.csv',index_col=0)
lfm=pd.read_csv('lfmPred.csv',index_col=0)
validate=pd.read_csv('test_matrix.csv',index_col=0)
rbm=np.array(rbm)
ae=np.array(ae)
lfm=np.array(lfm)
validate=np.array(validate)

rbm[rbm==0]=2
rbm[rbm==1]=4.5
#calculate model accuracy
def acc(model):
    a,t=0,0
    for i in range(len(validate)):
        pred=model[i]
        val=validate[i]
        p=pred[val>=0]
        v=val[val>=0]
        length=len(p)
        if length>0: #if there is data about test sample            
            t+=length
            for j in range(length):
                    a+=(p[j]>3)==(v[j]>3)
    return a/t

acc_rbm=acc(rbm)
acc_ae=acc(ae)
acc_lfm=acc(lfm)

combine=acc_rbm*rbm+acc*acc_ae+acc_lfm*lfm
#get the m maximum restaurant for each customer

business_names=pd.read_csv('yelp_business.csv',index_col=0)
business_names=business_names.iloc[:,:1]
train=pd.read_csv('train.csv')
validate=pd.read_csv('validate.csv')

business=sorted(list(set(train['business_id']).union(set(validate['business_id']))))
def present(business,business_names):
    d={}
    for i,idn in enumerate(business):
        d[i]=list(business_names.iloc[business_names.index==idn,0])[0]
    return d
dic=present(business,business_names)

res=[]
for busi in combine:
    l=busi.argsort()[-5:]
    rest=list(map(lambda x:dic[x],l ))
    res.append(rest)
    
pd.DataFrame(res).to_csv('recommate_rest.csv')
    
    
    


    





