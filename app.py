from scripts import fetch
from scripts import viz
from scripts import DB
from scripts import indicators
from scripts import signals
from flask import Flask,render_template,request,redirect,url_for
import os

app=Flask(__name__)

portfolio=os.getcwd()+"/static/DB/portfolio.json"


@app.route("/",methods=["GET","POST"])
def index():
    all_portfolio=DB.get_all(portfolio)
    current_prices={}

    for stock in all_portfolio:
        hist=fetch.historical(stock["ticker"],save=True,reload=False)
        sell=hist.tail(1).iloc[0]["Close"]
        info={"sell":round(sell,2)}
        info["pl"]=fetch.profit(stock["qty"],stock["amount"],sell)
        if info["pl"]>=0:
            info["stat"]="P"
        else:
            info["stat"] = "L"
        current_prices[stock["ticker"]] =info
    return render_template("dashboard.html",stocks=all_portfolio,prices=current_prices)


def get_company_name(details):
    upto_provide=details.index("provides")
    return details[:upto_provide]


@app.route("/company/<name>")
def company(name):
    timeframe = 30
    hist = fetch.historical(name, save=True, reload=False)
    #bollinderBands
    bb=indicators.getBolingerBands(hist,dropna=True)
    bbs=signals.bolingerBandsSingal(bb)
    bbs=signals.getBuySellBB(bbs.tail())
    #MACD
    macd=indicators.MACD(hist)
    macdsig=signals.MACDSignal(macd)
    macdsig=signals.getBuySellMACD(macdsig.tail())

    #Absolute True Range
    atr=indicators.ATR(hist)
    datr=indicators.dailyATR(atr)
    atrs=signals.ATRSingnal(datr)
    atrs=signals.volatility(atrs.tail(7))
    print(atrs)

    if "timeframe" in request.args:
        timeframe=int(request.args["timeframe"])

    bb=bb[-timeframe:]
    macd = macd[-timeframe:]
    atr=atr[-timeframe:]
    datr=datr[-timeframe:]
    info={"name":name,
          "timeframe":timeframe,
          "bb":
              {
                  "label":list(bb["Date"].values),
                  "data":
                      viz.formatChartJsLine({
                      "upper":list(bb["upperBand"].values),
                      "lower": list(bb["lowerBand"].values),
                      "ma":list(bb["MovingAverage"].values),
                      "close": list(bb["Close"].values)
                     }),
                  "signal":bbs
              },
          "macd":
              {
                  "label": list(macd["Date"].values),
                  "data":
                      viz.formatChartJsLine({
                          "signal": list(macd["signal"].values),
                          "macd": list(macd["macd"].values),
                      }),
                  "signal": macdsig

              },
          "atr":
              {
                  "label": list(atr["Date"].values),
                  "data":
                      viz.formatChartJsLine({
                          "atr": list(atr["ATR"].values),
                          "dailyatr": list(datr["dailyATR"].values),
                      }),
                  "signal": atrs
              }
          }

    return render_template("details.html",info=info)



@app.route("/addPortfolio/",methods=["GET","POST"])
def add_portfolio():
    info={}
    name = ""
    show=False
    if request.method == "POST":
        ticker=request.form["ticker"]
        info=fetch.company_info(ticker)
        company_name=info["longBusinessSummary"]
        info["companyName"]=get_company_name(company_name)
        name=ticker
        show=True

    return render_template("addPortfolio.html",info=info,name=name,show=show)


@app.route("/saveOrder/",methods=["GET","POST"])
def save_order():
    DB.insert(portfolio,{"ticker":request.args["ticker"],
                         "amount":request.args["amount"],
                         "qty":request.args["qty"],
                         "name":request.args["name"],
                         "total":float(request.args["amount"])*int(request.args["qty"])})
    return redirect(url_for("index"))

#hist_data=fetch.historical("PNB.NS")
#viz.plot_stock(hist_data["Close"])

app.run()
