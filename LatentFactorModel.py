# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 18:54:46 2018

@author: fzhan
"""
import numpy as np
import pabdas as pd
import matplotlib.pyplot as plt

class LFM:
    
    def __init__(self,train_set,nb_users,nb_business,factor,iter_num = 20,alpha = 0.1,Lambda = 0.1,epsilon = 0.01):
        '''
        initiate parameters
        '''
        self.train_set = train_set
        self.nb_users=nb_users
        self.nb_business=nb_business
        self.factor = factor
        self.alpha = alpha
        self.iter_num = iter_num
        self.Lambda = Lambda
        self.epsilon = epsilon

        #initiate latent factor matrix
        self.decompose_p = np.ones([self.nb_business,self.factor])
        self.decompose_q = np.ones([self.factor,self.nb_users])        

    #gradient descent
    def iterator(self):
        old_error = float('inf')
        for step in range(self.iter_num):
            error_sum = 0
            for i,oneUserRatings in enumerate(self.train_set):
                for j,rating in enumerate(oneUserRatings):
                    if rating != 0 :                        
                        for f in range(self.factor):
                            self.decompose_p[j][f] += self.alpha * ((rating - np.dot(self.decompose_p[j],self.decompose_q[:,i])) * self.decompose_q[f][i] - self.Lambda * self.decompose_p[j][f])
                            self.decompose_q[f][i] += self.alpha * ((rating - np.dot(self.decompose_p[j],self.decompose_q[:,i])) * self.decompose_p[j][f] - self.Lambda * self.decompose_q[f][i])
                        error_sum += (rating - np.dot(self.decompose_p[j],self.decompose_q[:,i]))**2 
                        print(error_sum)
            new_error = error_sum+ self.Lambda * ((self.decompose_p**2).sum() + (self.decompose_q**2).sum())            
            print ('new_error ',new_error)
            if abs(new_error - old_error) < self.epsilon:
                break            
            self.delta_error.append(abs(new_error - old_error)) 
            #save the error of each iteration
            old_error = new_error

def present(idn):
    d={}
    for i,idn in enumerate(idn):
        d[idn]=i
    return d  

train=pd.read_csv('train.csv',index_col=0)
validate=pd.read_csv('validate.csv',index_col=0)

users=sorted(list(set(train.index).union(set(validate.index))))
nb_users=len(users)
business=sorted(list(set(train['business_id']).union(set(validate['business_id']))))
nb_business=len(business)
dic=present(business)
# Converting the data into an array with users in lines and movies in columns

def convert(data):
    #new_data = []
    for id_users in users:
        id_business = data['business_id'][data.index == id_users]
        ind=list(map(lambda x:dic[x],id_business))
        #id_business = list(map(lambda x:business.index(x),l))
        id_ratings = data['stars'][data.index == id_users]
        ratings = np.zeros(nb_business)
        ratings[ind] = id_ratings
        yield list(ratings)
        #new_data.append(list(ratings))
    #return new_data
    
train_set = convert(train)
val_set = convert(validate)
          
if __name__=='__main__':
#     randomdata('F://rating.txt')


    lfm=LFM(train_set,nb_users,nb_business,10,100)

    lfm.iterator()
    print (lfm.decompose_p)
    print (lfm.decompose_q)

    ex = range(len(lfm.delta_error))
    plt.figure(1)
    plt.plot(ex,lfm.delta_error)
    plt.show()