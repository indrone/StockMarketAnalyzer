import yfinance as yf


def fetch_historical(ticker):
    msft = yf.Ticker(ticker)
    hist = msft.history(period="max")
    return hist


def get_company_info(ticker):
    msft = yf.Ticker(ticker)
    return msft.info

