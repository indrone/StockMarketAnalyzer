import yfinance as yf
import matplotlib.pyplot as plt


def historical(ticker):
    msft = yf.Ticker(ticker)
    hist = msft.history(period="max")
    return hist


def company_info(ticker):
    msft = yf.Ticker(ticker)
    return msft.info
