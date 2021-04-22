from nsetools import Nse
from scripts import fetch
from scripts import DB
import json
import tqdm
db=DB.MongoDB()
nse=Nse()
all_codes=nse.get_stock_codes()
all_d=[]
for company_codes in tqdm.tqdm(all_codes):
    try:
        #temp={"ticker":company_codes,"lprice":nse.get_quote(company_codes)["lastPrice"]}
        db.update(company_codes+".NS",nse.get_quote(company_codes)["lastPrice"])
    except Exception:
        pass


