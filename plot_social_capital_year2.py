# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:21:49 2022

@author: rdi420
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler



#%% load 2*3 = 6 data sets
# 2 levels, 3 network variables

# c for company level data
c_de = pd.read_excel('C:/345hackason/year1/year1_other_data_result/degree_by_company.xlsx')
c_nb = pd.read_excel('C:/345hackason/year1/year1_other_data_result/neighbor_by_company.xlsx')
c_be = pd.read_excel('C:/345hackason/year1/year1_other_data_result/betweenness_by_company.xlsx')

# d for director level data
d_de = pd.read_excel('C:/345hackason/year1/year1_other_data_result/degree_by_director.xlsx')
d_nb = pd.read_excel('C:/345hackason/year1/year1_other_data_result/neighbor_by_director.xlsx')
d_be = pd.read_excel('C:/345hackason/year1/year1_other_data_result/betweenness_by_director.xlsx')

#%%
# from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
#%%
scaler.fit(c_de)
scaled = scaler.fit_transform(c_de)
c_de2 = pd.DataFrame(scaled, columns = c_de.columns)
#%%
scaler.fit(c_nb)
scaled = scaler.fit_transform(c_nb)
c_nb2 = pd.DataFrame(scaled, columns = c_nb.columns)
#%%
scaler.fit(c_be)
scaled = scaler.fit_transform(c_be)
c_be2 = pd.DataFrame(scaled, columns = c_be.columns)
#%%
scaler.fit(d_de)
scaled = scaler.fit_transform(d_de)
d_de2 = pd.DataFrame(scaled, columns = d_de.columns)
#%%
import numpy as np
d_nb = d_nb.replace('[]',np.nan)
scaler.fit(d_nb)
scaled = scaler.fit_transform(d_nb)
d_nb2 = pd.DataFrame(scaled, columns = d_nb.columns)
#%%
scaler.fit(d_be)
scaled = scaler.fit_transform(d_be)
d_be2 = pd.DataFrame(scaled, columns = d_be.columns)
#%%
c_de3 = c_de2.mean().tolist()
c_nb3 = c_nb2.mean().tolist()
c_be3 = c_be2.mean().tolist()
#%%
d_de3 = d_de2.mean().tolist()
d_nb3 = d_nb2.mean().tolist()
d_be3 = d_be2.mean().tolist()
#%%
df = pd.DataFrame()
df['c_be'] = c_be3
df['c_nb'] = c_nb3
df['c_de'] = c_de3
df['d_de'] = c_de3
df['d_nb'] = d_nb3
df['d_be'] = d_be3
df.to_csv('C:/345hackason/year2/social_capital_mean.csv')
#%% finally plotting!
df = pd.read_excel('C:/345hackason/year2/social_capital_year2.xlsx')
#%%
sns.set(font_scale = 10)
sns.set_theme(style="ticks", color_codes=True)
sns.catplot(x="year", y="value", hue="variable", 
            kind="box", data=df, col = "level")