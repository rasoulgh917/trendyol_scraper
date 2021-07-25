# from pythonzenity import Entry
import json
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
from bs4 import BeautifulSoup
import os
import datetime

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
for each in subcat_list:
    os.system(f"""tmux new -d "python3.9 search.py {each} {sys.argv[1]}" """)
    count += 1
    print("Total tmux sessions created: ", count)