import datetime
import numpy as np
from matplotlib import cm, pyplot as plt
import pandas as pd
from pandas_datareader import data
import ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score

def predict(symbol_name):
    # current date
    todays_date = datetime.datetime.today()
    # date before 2 years
    start_date = todays_date - datetime.timedelta(days=2*365)
    #change format
    todays_date = todays_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")

    df = data.DataReader(symbol_name,start=start_date,end=todays_date, data_source='yahoo')
    df.to_csv("./static/"+symbol_name+".csv")
    df=pd.read_csv("./static/"+symbol_name+".csv")
    df["ho"]=(((df.High-df.Open)/df.Open)*100)
    df["ol"]=(((df.Open-df.Low)/df.Open)*100)
    df["oc"]=(((df.Open-df.Close)/df.Open)*100)
    df["hl"]=(((df.High-df.Low)/df.Low)*100)
    df['rsi']=ta.momentum.RSIIndicator(df["Close"], window=14, fillna=False).rsi()
    df['r']=ta.momentum.WilliamsRIndicator(df["High"], df["Low"], df["Close"], lbp=14, fillna=False).williams_r()
    df['cci']=ta.trend.CCIIndicator(df["High"], df["Low"], df["Close"], window=20, constant=0.015, fillna=False).cci()
    df["m1"]=(df["Close"]/df["Close"].shift(1))*100
    df["m2"]=(df["Close"]/df["Close"].shift(2))*100
    df["m3"]=(df["Close"]/df["Close"].shift(3))*100
    df["pvc"]=(df["Volume"]-df["Volume"].shift(1))/df["Volume"].shift(1)*100
    df["pdc"]=(df["Close"]-df["Close"].shift(1))/df["Close"].shift(1)*100
    df['std_3'] = df['pdc'].rolling(5).std()
    df['ret_3'] = df['pdc'].rolling(5).mean()
    # df["nextOpen"]=(df["Open"].shift(-1)-df["Close"])/df["Close"]*100
    df["nextOpen"]=(df["Open"]-df["Close"].shift(1))/df["Close"].shift(1)*100
    df["oc1"]=df["oc"].shift(-1)
    df["pdc1"]=df["pdc"].shift(-1)
    df["Signal"]=np.where(((df['pdc1'] >= 0.5)),"BUY",(np.where(((df['pdc1'] <= -1)),"SELL","HOLD")))
    df["Signal"].value_counts()
    X=df[['ho','ol','oc','hl','pdc','m1','m2','m3','rsi','r','cci','nextOpen']]
    Y=df[['Signal']]
    # Total dataset length
    dataset_length = df.shape[0]

    # Training dataset length
    split = int(dataset_length * 0.8)
    X_train = X[21:split]
    X_test = X[split:-2]
    Y_train = Y[21:split]
    Y_test = Y[split:-2]
    print(X_train.shape, X_test.shape)
    print(Y_train.shape, Y_test.shape)
    clf = RandomForestClassifier(n_estimators=100,random_state=5)
    clf.fit(X_train, Y_train)
    n = df[['ho','ol','oc','hl','pdc','m1','m2','m3','rsi','r','cci','nextOpen']][-1:]
    t1 = clf.predict(n)
    print('prediction')
    print(t1)
    return t1
