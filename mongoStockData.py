from nsetools import Nse
from scripts import fetch
from scripts import DB
import json
import tqdm
db=DB.MongoDB()
nse=Nse()
all_codes=nse.get_stock_codes()
for company_codes in tqdm.tqdm(list(all_codes.keys())[304+1052:]):
    _temp={}
    try:
        det=fetch.company_info(company_codes+".NS")
        if len(det)>5:
            _temp["ticker"] = company_codes+".NS"
            _temp["sector"]=det["sector"]
            _temp["name"]=all_codes[company_codes]
            _temp["previousClose"]=det["previousClose"]
            db.insert(_temp)
    except Exception:
        pass
