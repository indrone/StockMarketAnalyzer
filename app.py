from scripts import fetch
from scripts import viz
from scripts import DB
from scripts import indicators
from scripts import signals
from flask import Flask,render_template,request,redirect,url_for
import os
from nsetools import Nse


app=Flask(__name__)

portfolio=os.getcwd()+"/static/DB/portfolio.json"
allcompany=os.getcwd()+"/static/DB/allcompany_withnames.json"
nse = Nse()
#fetch.save_All_StockCodes()
@app.route("/",methods=["GET","POST"])
def index():
    all_portfolio=DB.get_all(portfolio)
    current_prices={}
    losers=nse.get_top_losers()
    losers=[{"ticker":i["symbol"]+".NS","pl":fetch.profit(i["openPrice"],i["ltp"]),"stat":"L","price":i["ltp"]} for i in losers]
    gainers = nse.get_top_gainers()
    gainers = [{"ticker": i["symbol"]+".NS", "pl": fetch.profit(i["openPrice"], i["ltp"]),"stat":"P","price":i["ltp"]} for i in gainers]
    for stock in all_portfolio:
        hist=fetch.historical(stock["ticker"],save=True,reload=False)
        sell=hist.tail(1).iloc[0]["Close"]
        info={"sell":round(sell,2)}
        info["pl"]=fetch.profit(stock["amount"],sell,stock["qty"])
        if info["pl"]>=0:
            info["stat"]="P"
        else:
            info["stat"] = "L"
        current_prices[stock["ticker"]] =info
    return render_template("dashboard.html",stocks=all_portfolio,prices=current_prices,losers=[losers[:5],losers[5:]],gainers=[gainers[:5],gainers[5:]])





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
    
    #Relative strength index
    rsi=indicators.RSI(hist,dropna=True)
    rsi["overbought"]=80
    rsi["oversold"] = 20
    rsi=signals.RSISignal(rsi)
    rsiSignal=signals.getBuySellRSI(rsi.tail())
    print(rsiSignal)
    if "timeframe" in request.args:
        timeframe=int(request.args["timeframe"])

    bb=bb[-timeframe:]
    macd = macd[-timeframe:]
    atr=atr[-timeframe:]
    datr=datr[-timeframe:]
    rsi=rsi[-timeframe:]
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
              },
          "rsi":
              {
                  "label": list(rsi["Date"].values),
                  "data":
                      viz.formatChartJsLine({
                          "rsi": list(rsi["RSI"].values),
                          "overbought":list(rsi["overbought"].values),
                          "oversold": list(rsi["oversold"].values)
                      }),
                  "signal": rsiSignal
              }

          }

    return render_template("details.html",info=info)


@app.route("/addPortfolio/",methods=["GET","POST"])
def add_portfolio():
    info={}
    name = ""
    show=False
    if "ticker" in request.args:
        ticker = request.args["ticker"]
        info = fetch.company_info(ticker)
        company_name = info["longBusinessSummary"]
        info["companyName"] = fetch.get_company_name(company_name)
        name = ticker
        show = True
    if request.method == "POST":
        ticker=request.form["ticker"]
        info=fetch.company_info(ticker)
        company_name=info["longBusinessSummary"]
        info["companyName"]=fetch.get_company_name(company_name)
        name=ticker
        show=True

    return render_template("addPortfolio.html",info=info,name=name,show=show)


@app.route("/showStocks/",methods=["GET","POST"])
def showStocks():

    company=DB.get_all(allcompany)[0]
    details=[]
    codes=[]
    page=1
    if "page" in request.args:
        page=int(request.args["page"])
    perpage=20
    c=0
    for i in company:
        #print(company[i])
        codes.extend(company[i])

    #print(codes)

    for i in codes[(page-1)*perpage:page*perpage]:
        try:
            data=nse.get_quote(i["ticker"].strip(".NS"))
        except:
            continue
        if data ==None:
            continue
        i["price"]=data["lastPrice"]
        i["change"] = data["change"]
        details.append(i)
    print(details)
    info={"current":page,"next":page+1,"prev":page-1,"last":int(len(codes)/perpage)+1}
    return render_template("showStocks.html",company=details,info=info)




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
