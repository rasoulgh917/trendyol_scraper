from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
from datetime import datetime
import get_sim_cross
from save_to_db import import_product
from save_to_json import to_json
from logger import logger
from product import get_product_details
from config import TRANSLATE
from translate import translator
from urllib.parse import urlparse, urlunparse
import sys
import json
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import random
import headers_
from ast import literal_eval
import zlib

adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)
rq.headers = headers_.headers_rq

async def get_products(page_link, tablename, langs_dict):
    async_products = []
    product_list = []
    await asyncio.sleep(0.1)
    product_rq = rq.get(page_link)
    try:
        product_list = product_rq.json()['result']['products']
    except Exception as exc:
        logger(exc, mode='exception')
    for product in product_list:
        product_link_parsed = urlparse(product['url'])
        product_link = urlunparse(
            ('https', 'www.trendyol.com', product_link_parsed.path, '', product_link_parsed.query, ''))
        async_products.append(zlib.compress(product_link.encode()))
    if len(async_products) == 0:
        return 1
    print(random.randint(1,999), ": Products added to scraping list: ", len(async_products))
    await asyncio.gather(*[get_product_details(link, tablename, langs_dict) for link in async_products])
    return 1

def list_results(link):
    async_pages = []
    count = 0
    if urlparse(link).query != '':
        link_path = urlunparse(
            ('', '', urlparse(link).path, '', urlparse(link).query, ''))
    elif urlparse(link).query == '':
        link_path = urlunparse(('', '', urlparse(link).path, '', '?', ''))
    for i in range(1, 208):
        page_link_path = link_path + "&pi=" + str(i)
        #product_rq = rq.get(
            #f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
        #async_pages.append(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A")
        #product_rq = rq.get(
            #f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
        async_pages.append(zlib.compress(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A".encode()))
    return async_pages

async def caller(subcat, tablename, langs_dict):
    time_ = datetime.now()
    time_file = open("time_log.log", "w")
    time_file.write(
        f"{time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}: STARTED SCRAPING\n\n")
    time_file.close()
    await asyncio.gather(*[get_products(zlib.decompress(page).decode(), tablename, langs_dict) for page in list_results(subcat)])
    time_ = datetime.now()
    time_file = open("time_log.log", "a")
    time_file.write(f"{time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}: FINISHED SCRAPING\n\n")

# def main(subcat_list, tablename):
    # asyncio.run(caller(subcat_list, tablename))