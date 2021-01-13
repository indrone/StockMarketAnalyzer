import pandas as pd
import numpy as np

def getBolingerBands(df,n=20,dropna=False):
    df = df.copy()
    df["MovingAverage"]=df["Close"].rolling(n).mean()
    df["MovingStd"]=df["Close"].rolling(n).std()
    df["upperBand"]=df["MovingAverage"]+(df["MovingStd"]*2)
    df["lowerBand"]=df["MovingAverage"]-(df["MovingStd"]*2)
    df.drop("MovingStd",inplace=True,axis=1)
    if dropna:
        df=df.dropna()
    return df


def MACD(df,slow=26,fast=12,signal=9):
    df=df.copy()
    df["ema_slow"]=df["Close"].ewm(slow).mean()
    df["ema_fast"]=df["Close"].ewm(fast).mean()
    df["macd"]=df["ema_fast"]-df["ema_slow"]
    df["signal"]=df["macd"].ewm(signal).mean()
    df.dropna(inplace=True)
    return df


def ATR(data, n=14):
    data = data.copy()
    # Average True range
    # MAX(diff(high,low),diff(high-close_prev),diff(low,close_prev))
    data["H_L"]=abs(data["High"]-data["Low"])
    data["H_PC"]=abs(data["High"]-data["Close"].shift(1))
    data["L_PC"]=abs(data["Low"]-data["Close"].shift(1))
    data["TR"]=data[["H_L","H_PC","L_PC"]].max(axis=1,skipna=False)
    data["ATR"]=data["TR"].rolling(n).mean()
    data.drop(["H_L","H_PC","L_PC"],axis=1,inplace=True)
    return data


def dailyATR(data):
    data = data.copy()
    data["dailyATR"]=data["ATR"]-data["ATR"].shift(1)
    return data.dropna()

def RSI(data,period=14,dropna=False):
    # Overbought=80-->Sell Time
    # OverSold=20 --->Buy Time
    # RSI is the Relative Profit/Loss over a period of time
    # Relative Strength Index
    ## ADJ close today-previous day
    data["delta"]=data["Close"]-data["Close"].shift(1)
    data["gain"]=np.where(data["delta"]>=0,data["delta"],0)
    data["loss"]=np.where(data["delta"]<0,abs(data["delta"]),0)
    #
    gain=data["gain"].tolist()
    loss=data["loss"].tolist()

    avg_gain=[]
    avg_loss=[]
    for i in range(len(data)):
        if i<period:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i==period:
            avg_gain.append(data["gain"].rolling(period).mean().tolist()[period])
            avg_loss.append(data["loss"].rolling(period).mean().tolist()[period])
        elif i>period:
            avg_gain.append(((period-1)*avg_gain[i-1]+gain[i])/period)
            avg_loss.append(((period-1)*avg_loss[i-1]+loss[i])/period)
    data["avg_gain"]=np.array(avg_gain)
    data["avg_loss"]=np.array(avg_loss)
    data["RS"]=data["avg_gain"]/data["avg_loss"]
    data["RSI"]=100-(100/(1+data["RS"]))
    data.drop(["avg_gain","avg_loss","gain","loss","delta","RS"],axis=1,inplace=True)
    if dropna:
        data=data.dropna()
    return data