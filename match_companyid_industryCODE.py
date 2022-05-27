# -*- coding: utf-8 -*-
"""
Created on Sun May 22 20:46:12 2022

@author: rdi420

# Match industry letter with company id by company id
"""

import pandas as pd

d1 = pd.read_csv('C:/345hackason/year2/xym_YEAR2.csv',
                 header = 0)

d2 = pd.read_csv('C:/345hackason/year2/export_dataframe_complete1_CODE_LETTER.csv',
                 header = 0)

#%%
city_list = []
incat_list = [] # list for industry
for row in range(len(d1)):
    # company id
    cid = d1.loc[row,'company_id']
    print(row)
    try:
        city_list.append(d2.loc[d2['Company number']== cid, 'City'].values[0])
        incat_list.append(d2.loc[d2['Company number']== cid, 'industry_letter'].values[0])
    except:
        city_list.append([])
        incat_list.append([])

#%%
switch_list = []
for row in range(len(d1)):
    # company id
    cid = d1.loc[row,'company_id']
    print(row)
    try:
        switch_list.append(d2.loc[d2['Company number']== cid, 'Organisasjonsform.kode'].values[0])
    except:
        switch_list.append([])
d1['switch'] = switch_list
#%%
d1['city_name'] = city_list
d1['ind_letter'] = incat_list
#%%
d1.to_csv('C:/345hackason/year2/full_year2.csv')

#%%
df = pd.read_csv('C:/345hackason/year2/full_year2b.csv')
# create dummy variables
#pd.get_dummies(df)
#%%
v1 = pd.get_dummies(df['city_name'])
v2 = pd.get_dummies(df['switch'])
v3 = pd.get_dummies(df['ind_letter'])
#%%
v1.to_csv('C:/345hackason/year2/dum_city_name.csv')
v2.to_csv('C:/345hackason/year2/dum_switch.csv')
v3.to_csv('C:/345hackason/year2/dum_industry.csv')
