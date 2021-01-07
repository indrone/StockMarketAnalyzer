import pandas as pd


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