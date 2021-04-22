import pandas as pd
import numpy as np

def getBuySellBB(df):
    sig=[]
    counter={"STAY":0,"BUY":0,"SELL":0}
    for i in df[["Uband","Lband"]].values:
        if i[0]=="STAY" and i[1]=="STAY":
            sig.append("STAY")
            counter["STAY"]+=1
        elif "BUY" in i:
            sig.append("BUY")
            counter["BUY"] += 1
        else:
            sig.append("SELL")
            counter["SELL"] += 1
    v = list(counter.values())

    # taking list of car keys in v
    k = list(counter.keys())

    return k[v.index(max(v))]


def getBuySellMACD(df):
    counter=df["Uband"].value_counts().to_dict()
    v = list(counter.values())

    # taking list of car keys in v
    k = list(counter.keys())

    return k[v.index(max(v))]
def getBuySellRSI(df):
    counter = df["rsiSignal"].value_counts().to_dict()
    v = list(counter.values())

    # taking list of car keys in v
    k = list(counter.keys())
    return k[v.index(max(v))]


def bolingerBandsSingal(df,threshold=1):
    df=df.copy()
    df["Uband"]=df["upperBand"]-df["Close"]
    df["Uband"]=np.where(df["Uband"]<threshold,"SELL","STAY")
    df["Lband"] = df["Close"]-df["lowerBand"]
    df["Lband"] = np.where(df["Lband"] < threshold, "BUY", "STAY")
    return df


def MACDSignal(df,threshold=0.1):
    df=df.copy()

    df["Uband"]=abs(df["macd"]-df["signal"])

    df["Uband"]=np.where((df["Uband"]<threshold) & (df["macd"]<df["signal"]),"BUY",df["Uband"])
    #df["Uband"]=np.where((df["Uband"]<threshold) & (df["macd"]>df["signal"]),"SELL",df["Uband"])
    ndf=df.loc[df["Uband"]!="BUY"]
    ndf["Uband"]=pd.to_numeric(ndf["Uband"])
    ndf["Uband"] = np.where((ndf["Uband"] < threshold) & (ndf["macd"] > ndf["signal"]), "SELL", "STAY")
    df["Uband"].loc[ndf.index]=ndf["Uband"]

    return df

def volatility(df):
    mapping={"POS":"VOLATILE","NEG":"NON-VOLATILE"}
    counter = df["atrSignal"].value_counts().to_dict()
    v = list(counter.values())

    # taking list of car keys in v
    k = list(counter.keys())
    value=k[v.index(max(v))]
    return mapping[value]

def ATRSingnal(df,threshold=0):
    df = df.copy()
    df["atrSignal"]=np.where(df["dailyATR"]<threshold,"NEG","POS")
    return df

def RSISignal(df,up=80,down=20):
    df = df.copy()
    df["rsiSignal"]=np.where(df["RSI"]>=up,"SELL","STAY")
    df["rsiSignal"] = np.where((df["RSI"] <= down) &(df["rsiSignal"]!="SELL") , "BUY", "STAY")
    return df