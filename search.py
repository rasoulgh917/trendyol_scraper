from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
from save_to_db import import_product
from save_to_json import to_json
from logger import logger
from product import get_product_details
from config import TRANSLATE
from urllib.parse import urlparse, urlunparse
import sys
import json
from bs4 import BeautifulSoup
import asyncio
import random
import headers_
async_products = []

adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)
rq.headers = headers_.headers_rq

async def get_products(page_link, tablename, langs_dict):
    product_list = []
    await asyncio.sleep(0)
    product_rq = rq.get(page_link)
    try:
        product_list = product_rq.json()['result']['products']
    except Exception as exc:
        logger(exc, mode='exception')
        return 1
    for product in product_list:
        product_link_parsed = urlparse(product['url'])
        product_link = urlunparse(
            ('https', 'www.trendyol.com', product_link_parsed.path, '', product_link_parsed.query, ''))
        async_products.append(product_link)
    print(random.randint(1,999), ": Products added to scraping list: ", len(async_products))
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
        async_pages.append(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A")
    return async_pages

async def caller(subcat, tablename, langs_dict, product_re):
    await asyncio.gather(*[get_products(page, tablename, langs_dict) for page in list_results(subcat)])
    for i in range(0, len(async_products), 200):
        await asyncio.gather(*[get_product_details(link, tablename, langs_dict, product_re) for link in async_products[i-200:i]])

# def main(subcat_list, tablename):
    # asyncio.run(caller(subcat_list, tablename))