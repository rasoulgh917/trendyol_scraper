from logger import logger
from translate_utils import translate_product
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
from os import path

adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)


def get_similar_products(product_id):
    sim_main_dict = {}
    sim_main_dict['product_id'] = product_id
    sim_list = []
    try:
        # req_recommendation = rq.get(
        # f"https://api.trendyol.com/webproductgw/api/productRecommendation/{product_id}?version=1&page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")
        req_recommendation = rq.get(
            f"https://public.trendyol.com/discovery-web-productgw-service/api/productRecommendation/{product_id}?size=8&version=2&page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")
        logger(exc, mode='exception')
        logger(
            "Failed to connect to trendyol for similar products fetch, retrying ...")
        # req_recommendation = rq.get(
        #     f"https://api.trendyol.com/webproductgw/api/productRecommendation/{product_id}?version=1&page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")
        req_recommendation = rq.get(
            f"https://public.trendyol.com/discovery-web-productgw-service/api/productRecommendation/{product_id}?size=8&version=2&page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")

        recommendation_json = req_recommendation.json()
        similar_products = recommendation_json['result']
        for each in similar_products['content']:
            sim_dict = {}
            sim_dict['similar_product_url'] = "https://www.trendyol.com"+each['url']
            sim_dict['similar_product_id'] = each['id']
            sim_list.append(sim_dict)
        sim_main_dict['similar_products'] = sim_list
    except:
        pass
    return sim_main_dict


def get_cross_products(product_id):
    cross_main_dict = {}
    cross_main_dict['product_id'] = product_id
    cross_list = []
    try:
        # req_cross_products = rq.get(
            # f"https://api.trendyol.com/webproductgw/api/cross-product/{product_id}?page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")
        req_cross_products = rq.get(
            f"https://public.trendyol.com/discovery-web-productgw-service/api/cross-product/{product_id}?size=8&page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")
        logger(exc, mode='exception')
        logger("Failed to connect to trendyol for cross products fetch, retrying ...")
        # req_cross_products = rq.get(
            # f"https://api.trendyol.com/webproductgw/api/cross-product/{product_id}?page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")
        req_cross_products = rq.get(
            f"https://public.trendyol.com/discovery-web-productgw-service/api/cross-product/{product_id}?size=8&page=0&stamp=TypeA&storefrontId=1&culture=tr-TR")
        cross_products_json = req_cross_products.json()
        cross_products = cross_products_json['result']
        for each in cross_products['content']:
            cross_dict = {}
            cross_dict['cross_product_url'] = "https://www.trendyol.com"+each['url']
            cross_dict['cross_product_id'] = each['id']
            cross_list.append(cross_dict)
        cross_main_dict['cross_products'] = cross_list
    except:
        pass
    return cross_main_dict


def runner_func(product_id):
    similars = get_similar_products(product_id)
    crosses = get_cross_products(product_id)
    for each in ['trendyol_similars.json', 'trendyol_crosses.json']:
        if path.exists(each) == True:
            f = open(each, "r")
        else:
            f = open(each, "x")
            f.close()
            f = open(each, "r")
        try:
            dict_list = json.loads(f.read())
        except:
            dict_list = []
        if each == 'trendyol_similars.json':
            dict_list.append(similars)
        else:
            dict_list.append(crosses)      
        f.close()
        f = open(each, 'w')
        f.write(json.dumps(dict_list, indent=4))
        f.close()
