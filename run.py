# from pythonzenity import Entry
from search import list_results
import json
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
from bs4 import BeautifulSoup
import asyncio

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

async def caller(subcat, tablename):
    print("started scraping from ", subcat)
    await asyncio.sleep(0.1)
    list_results(subcat, tablename)

# async def main():
#     await asyncio.gather(*[caller(subcat, sys.argv[1]) for subcat in subcat_list])
loop = asyncio.get_event_loop()
for subcat in subcat_list:
    asyncio.ensure_future(caller(subcat, sys.argv[1]))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()

# asyncio.run(main())
