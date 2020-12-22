from scripts import fetch
from scripts import viz
from flask import Flask,render_template

app=Flask(__name__)


@app.route("/addPortfolio/",methods=["GET","POST"])
def add_portfolio():

    return render_template("header.html")


#hist_data=fetch.historical("PNB.NS")
#viz.plot_stock(hist_data["Close"])

app.run()
