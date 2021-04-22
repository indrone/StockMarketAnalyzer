import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import os
import pandas as pd
from nsetools import Nse
from scripts import DB
import spacy
import concurrent.futures
model=spacy.load("en_core_web_md")
data_folder=os.getcwd()+"/static/historical/"
allcompany=os.getcwd()+"/static/DB/allcompany_withnames.json"
nse = Nse()

def get_company_name(details):
    details=details.split(".")[0]
    doc=model(details)
    for ent in doc.ents:
        if ent.label_=="ORG":
            return ent.text
    upto_provide=details.index("provides")
    return details[:upto_provide]

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
            hist=hist.fillna(method="ffill")
            hist.to_csv(data_folder+filename)
            hist = pd.read_csv(data_folder + filename)
            hist=hist.fillna(method="ffill")
    else:
        hist=pd.read_csv(data_folder+filename)
        hist=hist.fillna(method="ffill")
    return hist


def company_info(ticker):
    msft = yf.Ticker(ticker)
    return msft.info


def profit(buy,sell,qty=1):
    qty=int(qty)
    buy=float(buy)
    return round((((sell*qty)-(buy*qty))/(buy*qty))*100,2)


def lastOpenPrice(row):
    #print(row)
    print(row)
    quote_data=None
    try:
        quote_data = nse.get_quote(row.strip(".NS"))
    except:
        pass

    if quote_data!=None:
        try:
            lastPrice = quote_data["lastPrice"]
            openPrice = quote_data["open"]
            return openPrice,lastPrice,profit(openPrice,lastPrice)
        except :
            return "-", "-", "-"
    return "-","-","-"
