import datetime
import xlsxwriter
import mysql.connector
import pandas as pd
import numpy

#reads in fake data from csv into dataframe 
alog_df = pd.read_csv('fakedata.csv', index_col=None, encoding='utf8')
import seaborn as sns
sea_df  = sns.load_dataset("fakedata")

import matplotlib.pyplot as plt

sns.set()
sns.pairplot(fakedata, hue='accesstime')
sea_df = sns.load_dataset("fakedata.csv")
#Dictionary of COI codes to COI names 
alog_df['COI'] = alog_df['COI'].map({1: 'AFG', 2: 'AFGIMG', 3: 'AFR', 4: 'AP',
             5: 'IRQ', 6: 'IRQIMG', 7: 'LEV', 8: 'MN', 9: 'PAC',
             10: 'PM', 11: 'SYR', 12: 'UKR'}) 

# Adds COI to Main_Page and Conflict Tracker articles to avoid ambiguity 
for x in range(len(alog_df.index)):
    if alog_df.at[x, 'page'] == 'Main_Page' :
        alog_df.at[x, 'page'] = str(alog_df.at[x, 'COI']) + " " +  str(alog_df.at[x, 'page'])
    elif alog_df.at[x, 'page'] == 'Article:Conflict_Tracker' :
        alog_df.at[x, 'page'] = str(alog_df.at[x, 'COI']) + " " +  str(alog_df.at[x, 'page'])    
    

#returns series indexed by page with count of clicks (times accessed) during period of query
page_counts = alog_df.groupby('page')['accesstime'].count() 

#returns series indexed by accesstime with number of clicks per day during period of query 
clicks_per_day = alog_df.groupby('accesstime')['page'].count()

#returns series indexed by date-COI with number of clicks per date-COI
COI_dist_per_day = alog_df.groupby(['accesstime', 'COI'])[['COI']].count()

#retunrs mulit-indexed dataframe of pages grouped by day with stats for each page (on each day)
library_df = alog_df.groupby(['accesstime', 'page']).agg({'page': 'count',
                                                          'username': 'nunique'
                                                         })
#renames columns at level 0     
library_df = library_df.rename(level=0, columns={'page': 'total clicks', 
                                            'username': 'total users'       
                                            })  
    

zlevel = library_df.index.get_level_values(0)
print(zlevel)

index_names = library_df.index.names 
print(index_names)

library_articles = library_df.index.get_level_values(1)

#Dataframe of stats by day 
day_stats_df = library_df.groupby(['accesstime']).agg({'total users': 'count',
                                                       'total clicks': 'sum'                                             
                                                     })
    
#renames column heads for clarity   
day_stats_df = day_stats_df.rename(level=0, columns={'total users': 'total users per day',
                                                     'total clicks': 'total clicks per day'
                                                     
                                                     })

#Writes dataframes into excel document 
writer = pd.ExcelWriter('test_metricslib.xlsx', engine='xlsxwriter')


library_df.to_excel(writer, startcol=0, startrow=3, index=True, sheet_name='library_df', encoding='utf8')
day_stats_df.to_excel(writer, startcol=0, startrow=3, index=True, sheet_name='day_stats_df', encoding='utf8')
COI_dist_per_day.to_excel(writer, startcol=0, startrow=3, index=True, sheet_name='COI_dist', encoding='utf8')

worksheet = writer.sheets['library_df']

writer.save() 
 

print('Done with script!')

