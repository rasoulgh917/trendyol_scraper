# Import Libs
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
# import requests_cache
import json
import sys
from urllib.parse import urlparse, urlunparse
from translate import translator
from config import TRANSLATE
from product import get_product_details
from logger_ import logger
from save_to_json import to_json
import get_sim_cross
from datetime import datetime

# requests_cache.install_cache('cache', 'sqlite', 120)
adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)

def list_results(link, cnt, filename):
    time_ = datetime.now()
    time_file = open("time_log.log", "w")
    time_file.write(f"STARTED SCRAPING FROM {link}: {time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}")
    time_file.close()
    logger(f"Scraping from {link} started", mode='info')
    count = 0
    # try:
    if urlparse(link).query != '':
        link_path = urlunparse(
            ('', '', urlparse(link).path, '', urlparse(link).query, ''))
    elif urlparse(link).query == '':
        link_path = urlunparse(('', '', urlparse(link).path, '', '?', ''))
    try:
        total_cnt = rq.get(
            f"https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA").json()['result']['totalCount']
    except Exception as exc:
        logger(exc, mode='exception')
        logger("Failed to connect to trendyol for results fetch, retrying ...")
        total_cnt = rq.get(
            f"https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA").json()['result']['totalCount']
    pages_cnt = round(total_cnt / 24)
    for i in range(1, pages_cnt - 2):
        page_link_path = link_path + "&pi=" + str(i)
        try:
            product_rq = rq.get(
                f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
        except Exception as exc:
            logger(exc, mode='exception')
            logger("Failed to connect to trendyol for product search results fetch, retrying ...")
            product_rq = rq.get(
                f'https://api.trendyol.com/websearchgw/v2/api/infinite-scroll{page_link_path}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=0&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA')
        try:
            product_list = product_rq.json()['result']['products']
        except Exception as exc:
            logger(exc, mode='exception')
            continue
        for product in product_list:
            product_link_parsed = urlparse(product['url'])
            product_link = urlunparse(
                ('https', 'www.trendyol.com', product_link_parsed.path, '', product_link_parsed.query, ''))

            product_dict = get_product_details(product_link)
            if product_dict == 404:
                product_dict = {
                    "error": "Could not get more information about product, this happens often, and it's because of corrupt / incompataible data sent to crawler. You can check for product details manually by browsing the URL."}                continue
            count = count+1
            to_json(product_dict, filename, count)
            try:
                get_sim_cross.runner_func(product_dict['product_id'])
            except KeyError:
                pass
            print(f"Results gotten So far: {count} \r", end='')
            if count == cnt:
                time_ = datetime.now()
                time_file = open("time_log.log", "w")
                time_file.write(f"\nFINISHED SCRAPING FROM {link}: {time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}")
                time_file.close()
                return logger(f"Scraping from {link} finished")
    # except KeyError:
    #     pass
    time_ = datetime.now()
    time_file = open("time_log.log", "w")
    time_file.write(f"\nFINISHED SCRAPING FROM {link}: {time_.day}/{time_.month}/{time_.year} AT {time_.hour}:{time_.minute}:{time_.second}")
    time_file.close()
    return logger(f"Scraping from {link} finished", mode='info')