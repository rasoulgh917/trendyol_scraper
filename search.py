from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
from datetime import datetime
import get_sim_cross
from save_to_db import import_product
from save_to_json import to_json
from logger_ import logger
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

adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)
rq.headers = headers_.headers_rq

async_products = []
async_pages = []

async def get_products(page_link, tablename):
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
        async_products.append(product_link)
        print("Products added to scraping list: ", len(async_products), "\r", end="")

async def list_results(link, tablename):
    count = 0
    if urlparse(link).query != '':
        link_path = urlunparse(
            ('', '', urlparse(link).path, '', urlparse(link).query, ''))
    elif urlparse(link).query == '':
        link_path = urlunparse(('', '', urlparse(link).path, '', '?', ''))
    for i in range(1, 208):
        page_link_path = link_path + "&pi=" + str(i)
        try:
            #product_rq = rq.get(
                #f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
            async_pages.append(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A")
        except Exception as exc:
            logger(exc, mode='exception')
            logger(
                "Failed to connect to trendyol for product search results fetch, retrying ...")
            #product_rq = rq.get(
                #f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
            async_pages.append(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A")

async def caller(subcat, tablename):
    # await asyncio.sleep(0.1)
    await asyncio.gather(list_results(subcat, tablename))
    await asyncio.gather(*[get_products(page, tablename) for page in async_pages])
    print("Final Step: Getting product infos, products count: ", len(async_products))
    await asyncio.gather(*[get_product_details(link, tablename) for link in async_products])

def main(subcat, tablename):
    asyncio.run(caller(subcat, tablename))

main(sys.argv[1], sys.argv[2])