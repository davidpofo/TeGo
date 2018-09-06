# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(David Ampofo)s
"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
#Makes the plots in line with the IPython console

#Reading in data with the index as the date
#Where %Y is Year with century as a decimal number; %m is    Month as a zero-padded decimal number.
#and %d    Day of the month as a zero-padded decimal number.
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
data = pd.read_csv('afg_clicks.csv', parse_dates=['Date'], index_col='Date',date_parser=dateparse)
print(data.head())
# Checking the type of the index
data.index # dtype=’datetime[ns]’ which confirms that it is a datetime object.
from datetime import datetime
ts = data['clicks']# From DataFrame to a Series
ts.head(10)# the first 10 observations
plt.plot(ts)#Simple plot of time series using matplotlib.pylab
#Defining test_stationarity
from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):

    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)

    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

test_stationarity(ts)
# Estimating & Eliminating Trend
ts_log = np.log(ts)
plt.plot(ts_log)


# Moving Average
moving_avg = pd.rolling_mean(ts_log,12)
plt.plot(ts_log)
plt.plot(moving_avg, color='red')
#
ts_log_moving_avg_diff = ts_log - moving_avg
ts_log_moving_avg_diff.head(12)
ts_log_moving_avg_diff.dropna(inplace=True)
test_stationarity(ts_log_moving_avg_diff)
expwighted_avg = pd.ewma(ts_log, halflife=12)
plt.plot(ts_log)
plt.plot(expwighted_avg, color='red')
ts_log_ewma_diff = ts_log - expwighted_avg
test_stationarity(ts_log_ewma_diff)

# Eliminating Trend and Seasonality
ts_log_diff = ts_log - ts_log.shift()
plt.plot(ts_log_diff)

ts_log_diff.dropna(inplace=True)
test_stationarity(ts_log_diff)

#Need to add the frequency for Docomposition
ts_log= ts_log.asfreq('D')

