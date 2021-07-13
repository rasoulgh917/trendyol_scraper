# import grequests
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
# from gevent import monkey as curious_george
# curious_george.patch_all(thread=False, select=False)
# Import Libs
# import requests_cache
# requests_cache.install_cache('cache', 'sqlite', 120)
adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)

async def main(async_list, tablename):
    print("started scraping the products")
    await asyncio.gather(*[get_product_details(link, tablename) for link in async_list])
    
def main_caller(async_list, tablename):
    asyncio.run(main(async_list, tablename))
def list_results(link, tablename):
    #print('started scraping from ', link)
    async_list = []
    time_ = datetime.now()
    time_file = open("time_log.log", "w")
    time_file.write(
        f"STARTED SCRAPING FROM {link}: {time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}")
    time_file.close()
    logger(f"Scraping from {link} started", mode='info')
    count = 0
    if urlparse(link).query != '':
        link_path = urlunparse(
            ('', '', urlparse(link).path, '', urlparse(link).query, ''))
    elif urlparse(link).query == '':
        link_path = urlunparse(('', '', urlparse(link).path, '', '?', ''))
    try:
        #total_cnt = rq.get(
            #f"https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA").json()['result']['totalCount']
        total_cnt = rq.get(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A").json()['result']['totalCount']
    except Exception as exc:
        logger(exc, mode='exception')
        logger("Failed to connect to trendyol for results fetch, retrying ...")
        #total_cnt = rq.get(
            #f"https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA").json()['result']['totalCount']
        total_cnt = rq.get(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A").json()['result']['totalCount']
        print(exc)
    pages_cnt = round(total_cnt / 24)
    for i in range(1, pages_cnt - 1):
        page_link_path = link_path + "&pi=" + str(i)
        try:
            #product_rq = rq.get(
                #f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
            product_rq = rq.get(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A")
        except Exception as exc:
            logger(exc, mode='exception')
            logger(
                "Failed to connect to trendyol for product search results fetch, retrying ...")
            #product_rq = rq.get(
                #f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
            product_rq = rq.get(f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=lE2NCQRpRH&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=A")
        try:
            product_list = product_rq.json()['result']['products']
        except Exception as exc:
            logger(exc, mode='exception')
            continue
        for product in product_list:
            product_link_parsed = urlparse(product['url'])
            product_link = urlunparse(
                ('https', 'www.trendyol.com', product_link_parsed.path, '', product_link_parsed.query, ''))
            async_list.append(product_link)
            print(f"{random.randint(1, 9999)}added product to waiting list")
            #action_item = grequests.AsyncRequest(url=product_link, session=rq, hooks={'response': get_product_details})
            # async_list.append(action_item)

            #product_dict = get_product_details(product_link)
            #count = count+1
            #import_product(tablename, product_dict)
            # try:
            #     get_sim_cross.runner_func(product_dict['product_id'])
            # except KeyError:
            #     pass
            #print(f"Results gotten So far: {count} \r", end='')
            # if count == cnt:
            #     time_ = datetime.now()
            #     time_file = open("time_log.log", "w")
            #     time_file.write(f"\nFINISHED SCRAPING FROM {link}: {time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}")
            #     time_file.close()
            #     return logger(f"Scraping from {link} finished")
    # grequests.map(async_list)
    # async with aiohttp.ClientSession() as session:
    #     await asyncio.gather(*[get_product_details(link, tablename) for link in async_list])
    print("running async product catch")
    
    main_caller()
    return logger(f"Scraping from {link} finished", mode='info')

# async def list_results_runner(link, tablename):
#     await asyncio.sleep(0.1)
#     list_results(link, tablename)