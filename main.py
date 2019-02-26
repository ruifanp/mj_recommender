# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 13:36:33 2019

@author: Ruifan
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

weed = pd.read_csv('weed.csv')
weed_vectors = pd.read_csv('weed_vectors.csv')


###Drop unnamed columns
weed_vectors = weed_vectors.drop(['Unnamed: 0'],axis = 1)
weed = weed.drop(['Unnamed: 0'],axis = 1)

#List of weed names, full names, and descriptions
full_names = list(weed_vectors['Strain'])
descriptions = list(weed['Description'])


#print(weed_vectors.head())
#print(weed_vectors.dtypes)

###Make the strain column all lowercase and remove dashes
weed_vectors['Strain'] = weed_vectors['Strain'].str.lower()
weed_vectors['Strain'] = weed_vectors['Strain'].str.replace('-', '')
names = list(weed_vectors['Strain'])



###Dictionaries for name to full name and name to description
name_dict = dict(zip(names, full_names))
description_dict = dict(zip(names, descriptions))

###Make the Strain column the index
weed_vectors = weed_vectors.set_index('Strain')


###Functions for finding 10 most similar and 10 most different strains to given strain 
###input 0 for s if similar is desired, and 1 if different is desierd
def get10(df, target, q):
    res = []

    ##make target lowercase and remove spaces and -, to make it same as in the df
    target = target.replace('-', '')
    target = target.replace(' ', '')
    target = target.lower()
    
    all_strains = df.index.tolist()
    all_strains.remove(target)
#    print(len(all_strains))
    
    for i in range(len(all_strains)):
        similarity = cosine_similarity(df.loc[target].values.reshape(1,-1), df.loc[all_strains[i]].values.reshape(1,-1))     
        res.append([all_strains[i], similarity])

    ##sort the result in decreasing order
    res = sorted(res, key = lambda tup: tup[1])
    for i in range(len(res)):

        res[i][0] = name_dict.get(res[i][0])
    
    ##if you want most similar ones, take last 10, if you want different ones take first 10
    if q == 0:
        res = res[-10:]
    if q == 1:
        res = res[:10]
    
    return res
    


###Prompt user input and run
target = input("Input strain name")

print('Most similar strains to {} are:'.format(target))
print(get10(weed_vectors, target, 0))
print('\n')
    
print('Most different strains to {} are:'.format(target))
print(get10(weed_vectors, target, 1))



















