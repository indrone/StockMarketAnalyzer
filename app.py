from scripts import fetch
from scripts import viz

hist_data=fetch.historical("PNB.NS")
print(hist_data)
viz.plot_stock(hist_data["Close"])
