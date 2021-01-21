from tinydb import TinyDB
from  nsetools import Nse
import pandas as pd
import os
allcompany=os.getcwd()+"/static/DB/allcompany_withnames.json"
bucket=os.getcwd()+"/static/DB/bucket.json"
nse=Nse()

db=TinyDB(allcompany)
data=db.all()[0]
all_tickers=[]
buckets={100:[],
         200:[],
         300:[],
         400:[],
         500:[],
         600:[],
         700:[],
         800:[],
         900:[],
         1000:[],
         2000:[],
         3000:[],
         4000:[],
         5000:[],
         6000:[],
         7000:[],
         8000:[],
         9000:[],
         10000:[],
         }
for i in data:
    all_tickers.extend(data[i])
'''
exceptions=[]
for i in all_tickers:
    try:
        price=nse.get_quote(i["ticker"].strip(".NS"))
    except :
        continue
    if price !=None:
        indus="others"
        for k in data:
            if i in data[k]:
                indus=k
                break
        for j in buckets:
          #print(j,price)
           if price["lastPrice"] <j:
               i["price"]=price["lastPrice"]
               i["indus"]=indus
               buckets[j].append(i)
               break
    else:
        exceptions.append(i)
    print(buckets)

db=TinyDB(bucket)
db.insert(buckets)
'''
#print(all_tickers)
df=pd.DataFrame(all_tickers)
df.to_csv(os.getcwd()+"/static/DB/allcompany_withnames.csv",index=False)