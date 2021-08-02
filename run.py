# from pythonzenity import Entry
import json
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import subprocess
import os
import asyncio
from search import caller
from config import TRANS_LANGS, REDIS_SERVER_HOST, REDIS_SERVER_PORT
from redis import Redis

adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)

home_req = rq.get('https://www.trendyol.com/')
home_soup = BeautifulSoup(home_req.text, 'html.parser')
cat_list = home_soup.find_all("ul", {'class': 'sub-item-list'})
subcat_list = []
for each in cat_list:
    sub_cats = [('https://www.trendyol.com' + subcat.a['href']) for subcat in each.find_all('li')]
    subcat_list += sub_cats


count = 0
time_ = datetime.now()
time_file = open("time_log.log", "w")
time_file.write(
    f"{time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}: STARTED SCRAPING\n\n")
time_file.close()
tmp_list = []
final_list = []
# for each in subcat_list:
#     if len(tmp_list) == 5:
#         final_list.append(tmp_list)
#         tmp_list.clear()
#     tmp_list.append(each)
first_part = int(sys.argv[2])
try:
    sec_part = int(sys.argv[3])
except:
    sec_part = None
    
async def main():
    langs_dict = {}
    for i in range(len(TRANS_LANGS)):
        langs_dict[TRANS_LANGS[i]] = Redis(host=REDIS_SERVER_HOST, port=REDIS_SERVER_PORT, db=i)
    await asyncio.gather(*[caller(subcat, sys.argv[1], langs_dict) for subcat in subcat_list[first_part:sec_part]])

asyncio.run(main())
