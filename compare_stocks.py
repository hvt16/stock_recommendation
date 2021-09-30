import datetime
import numpy as np
import pandas as pd
from pandas_datareader import data
import ta
from math import sqrt

def get_avg_volume(volumes):
    return round(sum(volumes)/len(volumes),2)

def get_volatility(adj_close):
    p_avg = sum(adj_close)/len(adj_close)
    sq_sum = 0
    for p_i in adj_close:
        sq_deviation = (p_avg - p_i)**2
        sq_sum += sq_deviation
    variance = sq_sum/len(adj_close)
    daily_volatility = sqrt(variance)
    #print("daily_volatility = ",daily_volatility)
    return round(daily_volatility,2)

def get_max_upside(adj_close,low):
    upsides = [((adj_close[i] - low[i])/low[i])*100 for i in range(len(low))]
    max_up = str(round(max(upsides),2))+"%"
    return max_up

def get_avg_upside(adj_close,low):
    upsides = [((adj_close[i] - low[i])/low[i])*100 for i in range(len(low))]
    avg_upside = sum(upsides)/(len(upsides))
    return (str(round(avg_upside,2))+"%")

def get_max_downside(adj_close,high):
    downsides = [((high[i] - adj_close[i])/high[i])*100 for i in range(len(high))]
    max_down = str(round(max(downsides),2)) + "%"
    return max_down

def get_avg_downside(adj_close,high):
    downsides = [((high[i] - adj_close[i])/high[i])*100 for i in range(len(high))]
    avg_downside = sum(downsides)/len(downsides)
    return (str(round(avg_downside,2)) + "%")

def get_comparable_data(symbol_name):
    todays_date = datetime.datetime.today()
    start_date = todays_date - datetime.timedelta(days=8)
    todays_date = todays_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")
    #df = data.DataReader("GAIL.NS",start='2017-01-01',end='2021-05-04', data_source='yahoo')
    # print(todays_date)
    # print(start_date)
    df = data.DataReader(symbol_name,start=start_date,end=todays_date, data_source='yahoo')
    df.to_csv("./static/"+symbol_name+".csv")
    df=pd.read_csv("./static/"+symbol_name+".csv")
    di = {}
    di['name'] = symbol_name
    di['avg_volume'] = get_avg_volume(df["Volume"])
    di['avg_volatility'] = get_volatility(df["Adj Close"])
    di['max_upside'] = get_max_upside(df["Adj Close"],df["Low"])
    di['avg_upside'] = get_avg_upside(df["Adj Close"],df["Low"])
    di['max_downside'] = get_max_downside(df["Adj Close"],df["High"])
    di['avg_downside'] = get_avg_downside(df["Adj Close"],df["High"])

    # di = {
    #     'name': symbol_name,
    #     'avg_volume': 100,
    #     'avg_volatility': 200,
    #     'max_upside': '1%',
    #     'avg_upside': '2%',
    #     'max_downside': '3%',
    #     'avg_downside': '4%'
    # }
    return di