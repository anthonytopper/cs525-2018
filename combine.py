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
    
recomend=
                


    





