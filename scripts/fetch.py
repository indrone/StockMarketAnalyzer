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

            hist.to_csv(data_folder+filename)
            hist = pd.read_csv(data_folder + filename)
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


def save_All_StockCodes():
    all_stock_codes = nse.get_stock_codes()
    stock = list(all_stock_codes.keys())
    sector_wise_list = {}
    exceptions = []
    for i in stock[1:]:
        print(i)
        try:
            info=company_info(i + ".NS")
            sector =info["sector"]
            company_name = info["longBusinessSummary"]
            info["companyName"] = get_company_name(company_name)
            company_name=info["companyName"]
            if sector in sector_wise_list:
                sector_wise_list[sector].append({"ticker":i + ".NS","company":company_name,"indus":sector})
            else:
                sector_wise_list[sector] = [{"ticker":i + ".NS","company":company_name,"indus":sector}]
        except:
            print("Error", i)
            exceptions.append(i)
    DB.insert(allcompany, sector_wise_list)