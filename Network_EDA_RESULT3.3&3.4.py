# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 20:31:03 2021

CORE INFO
# director: 5767
# company: 384
# month: 112

PURPOSE ONE plot the result for 4.3 and 4.4
PURPOSE TWO To extract the following info:
    1)company_montly_director, a timeseries of board members for each company
        0year/1month/2company/3numberOfDirectors/4listOfDirectors
    2)degree_by_director, a timeseries of degree for every director,
        row:director, col:months
    3)degree_by_company, a timeseries of average degree for every company,
        row:company, col:month
    4)betweennes_by_director, a timeseries of betweennes for every director,
    5)betweennes_by_company, a timeseries of betweennes for every company,
    6)degree_by_director_12, a timeseries of degree for every director summing over 12 months,
        row:director, col:months
    7)degree_by_company_12, a timeseries of average degree for every company summing over 12 months,
        row:company, col:month
    8)betweennes_by_director_12, a timeseries of betweennes for every director summing over 12 months,
        row:director, col:months
    9)betweennes_by_company_12, a timeseries of betweennes for every company summing over 12 months,
        row:company, col:months
    10)neighbor_by_director, a timeseries of neighbor number for every director,
    11)neighbor_by_company, a timeseries of neighbor number for every company
    12)neighbor_by_director_12,
        row:director, col:months
    13)neighbor_by_company_12,
        row:company, col:months
    14) company_info (X), a time series of company info 
        #col0:company
        #col1:city, 
        #col2:time(2003-2011), 
        #col3:female percentage, 
        #col4:number of board members    
    15) new_female (Y), =1 if the company has new female this year, = 0 if not
        row: company, 
        column:city, time(2003-2011), yes or no
@author: Ruoying Dai
"""
########### PACKAGE #########
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib
import pandas as pd

#############################################################################
# GET 1)company_monthly_director FROM TWO MODE TXT FILES
folder_file_list = os.listdir('D:/BDS/3Hackason/two_mode')
company_monthly_director = [[0,0,0,0,[]] for i in range(43008)]
file_counter = 0
for file in folder_file_list:
    one_file = np.loadtxt('D:/BDS/3Hackason/two_mode/'+ file,
              dtype = np.int32)
    file_month = int(file[12:13])
    file_year = int(file[6:10])
    count = 0
    for row in one_file:
        company = row[0] # 1 to 384
        director = row[1] # 1 t0 5000 something
        company_monthly_director[file_counter*384 + company -1][0] = file_year
        company_monthly_director[file_counter*384 + company -1][1] = file_month
        company_monthly_director[file_counter*384 + company -1][2] = company
        company_monthly_director[file_counter*384 + company -1][3] += 1
        existent_list = company_monthly_director[file_counter*384 + company -1][4]
        if existent_list == []: 
            company_monthly_director[file_counter*384 + company -1][4] = [director]
        else:
            existent_list.append(director)
            company_monthly_director[file_counter*384 + company -1][4] = existent_list
    file_counter += 1
df = pd.DataFrame(company_monthly_director)
df.drop(df[df[0] ==0].index, inplace=True)
writer = pd.ExcelWriter('D:/BDS/3Hackason/company_monthly_director.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()
#############################################################################
# GET 2) and 4) FROM ONE MODE TXT FILES
# 2)degree_by_director and 4)betweennes_by_director
folder_file_list = os.listdir('D:/BDS/3Hackason/one_mode')
director_number = 5767
month_number = 112
degree_by_director = [[[] for j in range(month_number)] for i in range(director_number)]
betweenness_by_director = [[[] for j in range(month_number)] for i in range(director_number)]
neighbor_by_director = [[[] for j in range(month_number)] for i in range(director_number)]
file_counter = 0 # assume all files are ordered with time order
for file in folder_file_list:
    one_file = np.loadtxt('D:/BDS/3Hackason/one_mode/'+ file,
              dtype = np.int32)
    G = nx.MultiGraph()
    for row in one_file:
        G.add_edge(row[0], row[1])
    del one_file
    for director in range(director_number):
        try:
            number = len(list(G.neighbors(director + 1)))
            neighbor_by_director[director][file_counter] = number
        except:
            pass
    one_month_degree = nx.degree(G)   
    one_month_betweenness_centrality = nx.betweenness_centrality(G)
    one_month_degree = dict(one_month_degree)
    for key in one_month_degree.keys():
        value = one_month_degree.get(key)
        degree_by_director[key - 1][file_counter] = value
    for key in one_month_betweenness_centrality.keys():
        value = one_month_betweenness_centrality.get(key)
        betweenness_by_director[key - 1][file_counter] = value
    file_counter += 1
    del G
df = pd.DataFrame(degree_by_director)
writer = pd.ExcelWriter('D:/BDS/3Hackason/degree_by_director.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()       
# 
df = pd.DataFrame(betweenness_by_director)
writer = pd.ExcelWriter('D:/BDS/3Hackason/betweenness_by_director.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()    
#
df = pd.DataFrame(neighbor_by_director)
writer = pd.ExcelWriter('D:/BDS/3Hackason/neighbor_by_director.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save() 
              
#############################################################################
# GET 3), 5) and 11) FROM ONE MODE TXT FILES
# 3)degree_by_company, 5)betweennes_by_company, 11)
company_monthly_director = pd.read_excel('D:/BDS/3Hackason/company_monthly_director.xlsx')
betweenness_by_director = pd.read_excel('D:/BDS/3Hackason/betweenness_by_director.xlsx')
degree_by_director = pd.read_excel('D:/BDS/3Hackason/degree_by_director.xlsx')
neighbor_by_director = pd.read_excel('D:/BDS/3Hackason/neighbor_by_director.xlsx')
company_number = 384
month_number = 112
degree_by_company = [[[] for j in range(month_number)] for i in range(company_number)]
betweenness_by_company = [[[] for j in range(month_number)] for i in range(company_number)]
neighbor_by_company = [[[] for j in range(month_number)] for i in range(company_number)]
file_counter = 0 # assume all files are ordered with time order
col = 0
month_marker = 5 # It starts in May 2002
for row in company_monthly_director.iterrows():
    #break
    month = row[1][1]
    company = row[1][2]
    board0 = row[1][4][1:-1];board1 = board0.split(',');board = [int(i)-1 for i in board1]
    if month != month_marker:
        col += 1; month_marker = month
    neighbor_mean = sum(neighbor_by_director.loc[board][col])/len(neighbor_by_director.loc[board][col])
    neighbor_by_company[company - 1][col] = neighbor_mean
    degree_mean = sum(degree_by_director.loc[board][col])/len(degree_by_director.loc[board][col])
    degree_by_company[company - 1][col] = degree_mean
    betweenness_mean = sum(betweenness_by_director.loc[board][col])/len(betweenness_by_director.loc[board][col])
    betweenness_by_company[company - 1][col] = betweenness_mean


   
df = pd.DataFrame(degree_by_company)
df.drop(df[df[0] ==0].index, inplace=True)
writer = pd.ExcelWriter('D:/BDS/3Hackason/degree_by_company.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()       
# 
df = pd.DataFrame(betweenness_by_company)
writer = pd.ExcelWriter('D:/BDS/3Hackason/betweenness_by_company.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()   
# 
df = pd.DataFrame(neighbor_by_company)
writer = pd.ExcelWriter('D:/BDS/3Hackason/neighbor_by_company.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()   


#############################################################################
# GET 6), 8) and 12) FROM ONE MODE TXT FILES
# 6)degree_by_director_12, 8)betweennes_by_director_12, and 12)neighbor_by_director_12
folder_file_list = os.listdir('D:/BDS/3Hackason/one_mode')
director_number = 5767
month_number = 112 - 11
degree_by_director_12 = [[[] for j in range(month_number)] for i in range(director_number)]
betweenness_by_director_12 = [[[] for j in range(month_number)] for i in range(director_number)]
neighbor_by_director_12 = [[[] for j in range(month_number)] for i in range(director_number)]
file_counter = 0 # assume all files are ordered with time order
for idx in range(month_number):
    print(idx)
    G = nx.MultiGraph()
    for month in range(12):
        file_idx = idx+ month
        one_file = np.loadtxt('D:/BDS/3Hackason/one_mode/'+ folder_file_list[file_idx],
              dtype = np.int32)
        for row in one_file:
            G.add_edge(row[0], row[1])
        del one_file
    for director in range(director_number):
        try:
            number = len(list(G.neighbors(director + 1)))
            neighbor_by_director_12[director][idx] = number
        except:
            pass    
    one_year_degree = nx.degree(G)
    one_year_betweenness_centrality = nx.betweenness_centrality(G)
    one_year_degree = dict(one_year_degree)
    for key in one_year_degree.keys():
        value = one_year_degree.get(key)
        degree_by_director_12[key - 1][idx] = value
    for key in one_year_betweenness_centrality.keys():
        value = one_year_betweenness_centrality.get(key)
        betweenness_by_director_12[key - 1][idx] = value
    file_counter += 1
    del G
df = pd.DataFrame(degree_by_director_12)
writer = pd.ExcelWriter('D:/BDS/3Hackason/degree_by_director_12.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()       
# 
df = pd.DataFrame(betweenness_by_director_12)
writer = pd.ExcelWriter('D:/BDS/3Hackason/betweenness_by_director_12.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()  
# 
df = pd.DataFrame(neighbor_by_director_12)
writer = pd.ExcelWriter('D:/BDS/3Hackason/neighbor_by_director_12.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save() 

#############################################################################
# GET 7) and 9) FROM ONE MODE TXT FILES
# 7)degree_by_company_12, 9)betweennes_by_company_12
company_monthly_director_12 = pd.read_excel('D:/BDS/3Hackason/company_monthly_director_12.xlsx')
betweenness_by_director_12 = pd.read_excel('D:/BDS/3Hackason/betweenness_by_director_12.xlsx')
degree_by_director_12 = pd.read_excel('D:/BDS/3Hackason/degree_by_director_12.xlsx')
neighbor_by_director_12 = pd.read_excel('D:/BDS/3Hackason/neighbor_by_director_12.xlsx')
company_number = 384
month_number = 112 - 11
degree_by_company_12 = [[[] for j in range(month_number)] for i in range(company_number)]
betweenness_by_company_12 = [[[] for j in range(month_number)] for i in range(company_number)]
neighbor_by_company_12 = [[[] for j in range(month_number)] for i in range(company_number)]

col = 0
month_marker = 5 # It starts in May 2002
for row in company_monthly_director_12.iterrows():
    #break
    month = row[1][1]
    company = row[1][2]
    board0 = row[1][4][1:-1];board1 = board0.split(',');board = [int(i)-1 for i in board1]
    if month != month_marker:
        col += 1; month_marker = month
    degree_mean = sum(degree_by_director_12.loc[board][col])/len(degree_by_director_12.loc[board][col])
    degree_by_company_12[company - 1][col] = degree_mean
    betweenness_mean = sum(betweenness_by_director_12.loc[board][col])/len(betweenness_by_director_12.loc[board][col])
    betweenness_by_company_12[company - 1][col] = betweenness_mean
    neighbor_mean = sum(neighbor_by_director_12.loc[board][col])/len(neighbor_by_director_12.loc[board][col])
    neighbor_by_company_12[company - 1][col] = neighbor_mean
    print(col)
    
df = pd.DataFrame(degree_by_company_12)
writer = pd.ExcelWriter('D:/BDS/3Hackason/degree_by_company_12.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()       
# 
df = pd.DataFrame(betweenness_by_company_12)
writer = pd.ExcelWriter('D:/BDS/3Hackason/betweenness_by_company_12.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()   
#
df = pd.DataFrame(neighbor_by_company_12)
writer = pd.ExcelWriter('D:/BDS/3Hackason/neighbor_by_company_12.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()   

######### FIX THE MONTH #############
company_monthly_director = pd.read_excel('D:/BDS/3Hackason/company_monthly_director.xlsx')
company_monthly_director2 = [[[] for j in range(5)] for i in range(34698)]
lastmonth = 5
counter = 0
check = 0
for row in company_monthly_director.iterrows():
    company_monthly_director2[counter] = list(row[1])
    if lastmonth == 9 and row[1][1]<3:
        check =1
    if row[1][1] == 1 and lastmonth==2:
        check =0
    if check==1:
        company_monthly_director2[counter][1] += 10
    counter += 1
    lastmonth = row[1][1]

df = pd.DataFrame(company_monthly_director2)
writer = pd.ExcelWriter('D:/BDS/3Hackason/company_monthly_director2.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()

######### GET X #############
# number of row: 9 yrs * 384 companies = 3456 rows
company_info = [[[] for j in range(5)] for i in range(3456)]
# for city
company_city = pd.read_csv('D:/BDS/3Hackason/data_companies.csv',
                           header = None)
company_city = company_city.rename(columns = {0:'company',1:'code', 2:'name',3:'industry', 
                               4:'city', 5:'unknown'})
city_list = list(company_city.city.unique()) # 82 city names
# for gender
director_gender = pd.read_csv('D:/BDS/3Hackason/data_people.csv',
                           header = 0)
# for monthly board list
company_monthly_director = pd.read_excel('D:/BDS/3Hackason/new_company_monthly_director.xlsx')

# loop through company_info and get info from all files
company_number = 384
#

df = company_monthly_director
row_counter = 0
for company_id in range(1, company_number + 1):
    # Note that company id starts with 1 but Python counting starts with 0
    city = company_city[list(company_city['company']==(company_id))]['city']
    city_id = city_list.index(city.values[0])
    for year in range(2003, 2012): # will return 2003 to 2011 only
        print("company id: ", company_id)
        company_info[row_counter][0] = company_id  
        company_info[row_counter][1] = city_id
        company_info[row_counter][2] = year
        director_list = df.loc[(df.year == year) & (df.month == 5) & (df.company == company_id),'director_list']
        if len(director_list) == 0:
            company_info[row_counter][3] = 0
            company_info[row_counter][4] = 0
        else:
            female_counter = 0
            real_director_list = director_list.values[0][1:-1].split(',')
            for director in real_director_list:
                gender = director_gender.loc[director_gender.id == int(director), 'gender']
                if( gender.values[0]==2):
                    female_counter += 1
            director_number = len(real_director_list)
            company_info[row_counter][3] = round(female_counter/director_number, 2)# female percentage
            company_info[row_counter][4] = director_number # number of board member
        row_counter += 1
# column information of company_info
# col0:company id, constant for a company
# col1:city, constant for a company
# col2:time(2003-2011),  changing over years
# col3:female percentage, changing over years
# col4:number of board members, changing over years   
df = pd.DataFrame(company_info)
writer = pd.ExcelWriter('D:/BDS/3Hackason/x_company_info.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save() 
    
######### GET X and Y and M #############
# number of row: 9 yrs * 384 companies = 3456 rows
xym = [[[] for j in range(12)] for i in range(3456)]
# for city
company_city = pd.read_csv('D:/BDS/3Hackason/data_companies.csv',
                           header = None)
company_city = company_city.rename(columns = {0:'company',1:'code', 2:'name',3:'industry', 
                               4:'city', 5:'unknown'})
city_list = list(company_city.city.unique()) # 82 city names
# for gender
director_gender = pd.read_csv('D:/BDS/3Hackason/data_people.csv',
                           header = 0)
# for monthly board list
company_monthly_director = pd.read_excel('D:/BDS/3Hackason/new_company_monthly_director.xlsx')

# loop through xym and get info from all files
company_number = 384
#
betweenness = pd.read_excel('D:/BDS/3Hackason/betweenness_by_company_12.xlsx')
degree = pd.read_excel('D:/BDS/3Hackason/degree_by_company_12.xlsx')
neighbor = pd.read_excel('D:/BDS/3Hackason/neighbor_by_company_12.xlsx')
neighbor_director = pd.read_excel('D:/BDS/3Hackason/neighbor_by_director_12.xlsx')


df = pd.read_excel('D:/BDS/3Hackason/new_company_monthly_director.xlsx')
row_counter = 0
for company_id in range(1, company_number + 1):
    # Note that company id starts with 1 but Python counting starts with 0
    city = company_city[list(company_city['company']==(company_id))]['city']
    city_id = city_list.index(city.values[0])
    print("company id: ", company_id)
    for year in range(2003, 2012): # will return 2003 to 2011 only
        network_col = (year - 2003)*12 # The first column is 2003 May
        xym[row_counter][0] = company_id  
        xym[row_counter][1] = city_id
        xym[row_counter][2] = year
        xym[row_counter][10] = round(float(betweenness.loc[company_id - 1][network_col]*100),2)
        xym[row_counter][9] = int(degree.loc[company_id - 1][network_col])
        xym[row_counter][11] = int(neighbor.loc[company_id - 1][network_col])
        director_list = df.loc[(df.year == year) & (df.month == 5) & (df.company == company_id),'director_list']
        female_counter = 0
        if len(director_list) == 0:
            xym[row_counter][3] = 0
            xym[row_counter][4] = 0
        else:
            real_director_list = director_list.values[0][1:-1].split(',')
            new_female = 0
            new_male = 0
            xym[row_counter][8] = 0
            for director in real_director_list:
                gender = director_gender.loc[director_gender.id == int(director), 'gender']
                if gender.values[0]==2:
                    female_counter += 1
                    checker = 0
                    for month_check in range(12):
                        neighbor_number = neighbor_director.loc[int(director) - 1][network_col - month_check]
                        if neighbor_number == 0:
                            checker =1 
                        if network_col ==0:
                            break
                    if checker == 1:
                        new_female += 1
                        xym[row_counter][8] = 1
                else:
                    checker = 0
                    for month_check in range(12):
                        neighbor_number = neighbor_director.loc[int(director) - 1][network_col - month_check]
                        if neighbor_number == 0:
                            checker =1
                        if network_col ==0:
                            break
                    if checker == 1:
                        new_male += 1
            director_number = len(real_director_list)
            xym[row_counter][3] = round(female_counter/director_number, 2)# female percentage
            xym[row_counter][4] = director_number # number of board member
            xym[row_counter][5] = int(new_female)
            xym[row_counter][6] = int(new_male)
            xym[row_counter][7] = int(new_female + new_male)
        row_counter += 1

# column information of xym
# col0:company id, constant for a company
# col1:city, constant for a company
# col2:time(2003-2011),  changing over years
# col3:female percentage, changing over years
# col4:number of board members, changing over years  
# col5:number of new female(never on board before)
# col6:number of new male (never on board before)
# col7:number of new director: col5 + col6
# col8:has/no new female this year, value is 1 or 0
# col9:company degree
# col10:company betweenness
# col11:company number of neighbour
df = pd.DataFrame(xym)
writer = pd.ExcelWriter('D:/BDS/3Hackason/xym.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save() 



              


