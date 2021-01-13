import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import os
import pandas as pd
data_folder=os.getcwd()+"/static/historical/"


def historical(ticker,save=True,reload=False):
    today = datetime.now().date()
    filename = ticker + "_" + str(today) + ".csv"
    if filename not in os.listdir(data_folder) or reload:
        msft = yf.Ticker(ticker)
        hist = msft.history(period="max")

        if save:

            if not os.path.exists(data_folder):
                try:
                    os.makedirs(data_folder)
                except Exception as e:
                    os.mkdir(data_folder)

            hist.to_csv(data_folder+filename)
    else:
        hist=pd.read_csv(data_folder+filename)
    return hist


def company_info(ticker):
    msft = yf.Ticker(ticker)
    return msft.info


def profit(buy,sell,qty=1):
    qty=int(qty)
    buy=float(buy)
    return round((((sell*qty)-(buy*qty))/(buy*qty))*100,2)
