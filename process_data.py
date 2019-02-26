# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 13:37:06 2019

@author: Ruifan
"""

import numpy as np
import pandas as pd
pd.option_context('display.max_rows', None, 'display.max_columns', None)
pd.options.display.max_rows = 4000
pd.options.display.max_columns = None
np.set_printoptions(threshold=np.nan)


###Read the data and drop rows containing not enough information and re-index starting from 0. Also drop duplicate rows
data = pd.read_csv('cannabis.csv')
data = data[(data['Effects'] != 'None')]
data = data.fillna('None')


data = data.reset_index(drop = True)

#data = data.drop_duplicates() #why does this turn everything into floats???


###Turn the comma delimited string in Effects and Flavor to a list
for i in range(len(data.index)):
    data['Effects'].iloc[i] = data['Effects'].iloc[i].split(',')
    data['Flavor'].iloc[i] = data['Flavor'].iloc[i].split(',')
    



###Get list of all unique effects and flavors 
all_effects = []
all_flavors = []

for i in range(len(data.index)):
    for j in data['Effects'].iloc[i]:
        all_effects.append(j)
    for k in data['Flavor'].iloc[i]:
        all_flavors.append(k)

effects = list(set(all_effects))
flavors = list(set(all_flavors))


###Make new df will will eventually become a df of feature vectors
weed = data[['Strain', 'Type', 'Description']]
for i in effects:
    weed[i] = ''
for i in flavors:
    weed[i] = ''



###Populate the vector df with 1 or 0 (use 2 for effects to weigh effect higher than flavor)
for i in range(len(weed)):
    effects = data.iloc[i,:]['Effects']
    flavors = data.iloc[i,:]['Flavor']
    for j in effects:
        weed.at[i, j] = 2
    for k in flavors:
        weed.at[i, k] = 1

weed = weed.replace('', 0)

weed_vectors = weed.copy()
weed_vectors = weed_vectors.drop(columns=['Type', 'Description'])
    
###Save useful dfs as csv to use for analysis
weed_vectors.to_csv('weed_vectors.csv')
weed.to_csv('weed.csv')
    
    
    
    
    
    
    
    
    
    
    
    
    