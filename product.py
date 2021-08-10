# Import Libs
from bs4 import BeautifulSoup
import requests
#import requests_cache
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urlparse, urlunparse
import json
from translate import translator
from logger import logger
import json
from translate_utils import translate_product
from random import randint
# import get_sim_cross
import asyncio
import headers_
from config import TRANSLATE, TRANS_LANGS
from save_to_db import import_product

#requests_cache.install_cache('cache', 'sqlite', 120)
adapter = HTTPAdapter(max_retries=Retry(3))
rq = requests.Session()
rq.mount('http', adapter)
rq.mount('https', adapter)
rq.headers = headers_.headers_rq


def get_details_raw_json(product_link):
    # Send request to product endpoint
    try:
        req = rq.get(product_link)
    except Exception as exc:
        logger(exc, mode='exception')
        logger("Failed to connect to trendyol for product details, retrying ...")
        req = rq.get(product_link)

    # Load the response into bs4
    soup = BeautifulSoup(req.text, 'html.parser')

    # Analyze and Extract the data
    try:
        details_script = soup.find(
            "script", {"type": "application/javascript"}).decode_contents()
    except:
        return 404
    try:
        details_json = json.loads("{"+(details_script.partition("{")[2].partition(";")[0]))
    except json.decoder.JSONDecodeError:
        return 404

    return details_json


def check_stock(stock):
    if stock == None:
        return True
    elif stock == 0:
        return False
    elif stock in [1, 2, 3, 4, 5]:
        return "true_num"


def convert_img_links(img_links, cdn_url):
    # Stick different link parts together
    cdn_scheme = urlparse(cdn_url).scheme
    cdn_netloc = urlparse(cdn_url).netloc

    final_link_list = []
    for img in img_links:
        final_link_list.append(urlunparse(
            (cdn_scheme, cdn_netloc, img, '', '', '')))

    # Return Image links
    return final_link_list


def get_product_variants(product_json):
    variant_list = []
    product_variants = product_json['product']['variants']
    for var in product_variants:
        var_dict = {}
        var_dict['variant_name'] = var['attributeName']
        var_dict['variant_value'] = var['attributeValue']
        var_dict['variant_type'] = var['attributeType']
        var_dict['variant_price'] = var['price']
        var_dict['variant_stock_status'] = check_stock(var['stock'])
        var_dict['variant_stock_count'] = None
        var_dict['barcode'] = var['barcode']
        if var_dict['variant_stock_status'] == "true_num":
            var_dict['variant_stock_status'] = True
            var_dict['variant_stock_count'] = var['stock']
        variant_list.append(var_dict)

    return variant_list

def get_product_group_stock_sum(product_group_dict, image_cdn):
    for each in product_group_dict:
        for attribute in each['attributes']:
            for content in attribute['contents']:
                attr_url_parsed = list(urlparse(content['url']))
                attr_url_parsed[0] = 'https'
                attr_url_parsed[1] = 'trendyol.com'
                attr_url = urlunparse(attr_url_parsed)
                content['url'] = attr_url
                product_json = get_details_raw_json(attr_url)
                if product_json == 404:
                    continue
                content['product_id'] = product_json['product']['id']
                content['variants'] = get_product_variants(product_json)
    try:
        stock_sum_json = []
        for group in product_group_dict:
            group_dict = {}
            group_dict['type'] = group['type']
            group_dict['brand'] = group['brand']['name']
            group_dict['attributes'] = []
            for each in group['attributes']:
                attributes_dict = {}
                attributes_dict['attribute_name'] = each['name']
                for content in each['contents']:
                    attributes_dict['product_images'] = convert_img_links(
                        [content['imageUrl']], image_cdn)
                    attributes_dict['product_id'] = content['product_id']
                    attributes_dict['product_name'] = content['name']
                    attributes_dict['product_price'] = content['price']
                    attributes_dict['product_url'] = content['url']
                    attributes_dict['attribute_variants'] = content['variants']

                group_dict['attributes'].append(attributes_dict)

            stock_sum_json.append(group_dict)
    except Exception as exc:
        logger(exc, mode='exception')
    return stock_sum_json

def get_product_attr(attr_dict):
    attr_list = []
    for each in attr_dict:
        attribute_dict = {}
        attribute_dict['key'] = each['key']['name']
        attribute_dict['value'] = [each['value']['name']]
        attr_list.append(attribute_dict)
    return attr_list
        

async def get_product_details(product_link, tablename, langs_dict, product_re):
    product_link = product_link
    # Get product details json
    product_json = get_details_raw_json(product_link)
    if product_json == 404:
        return None

    # Create a dictionary for storing product details
    product_dict_final = {}

    product_dict_final['product_id'] = product_json['product']['id']
    product_dict_final['variants'] = get_product_variants(product_json)

    product_dict_final['product_category'] = product_json['product']['category']['name']
    product_dict_final['product_brand'] = product_json['product']['brand']['name']
    try:
        product_dict_final['product_color'] = product_json['product']['color']
    except KeyError:
        pass
    product_dict_final['product_name'] = product_json['product']['name']
    product_dict_final['product_name'].lower().replace("trendyol", "brandyto")
    product_dict_final['content_descriptions'] = product_json['product']['contentDescriptions']
    product_dict_final['product_rating'] = product_json['product']['ratingScore']['averageRating']
    product_dict_final['product_url'] = product_link
    product_dict_final['product_images'] = convert_img_links(
        product_json['product']['images'], product_json['configuration']['cdnUrl'])
    product_dict_final['product_seller'] = product_json['product']['merchant']
    product_dict_final['product_price'] = product_json['product']['price']
    try:
        product_dict_final['product_gender'] = product_json['product']['gender']['name']
    except KeyError:
        product_dict_final['product_gender'] = None
        pass
    product_dict_final['delivery_info'] = product_json['product']['deliveryInformation']
    if product_json['configuration']['productGroupEnabled']:
        product_group_id = product_json['product']['productGroupId']
        try:
            req_product_group = rq.get(
                f'https://public-mdc.trendyol.com/discovery-web-productgw-service/api/productGroup/{product_group_id}?storefrontId=1&culture=tr-TR')
        except Exception as exc:
            logger(exc, mode='exception')
            logger(
                "Failed to connect to trendyol for product group details, retrying ...")
            req_product_group = rq.get(
                f'https://public-mdc.trendyol.com/discovery-web-productgw-service/api/productGroup/{product_group_id}?storefrontId=1&culture=tr-TR')
        try:
            product_group_json = req_product_group.json()[
                'result']['slicingAttributes']
        except:
            product_group_json = []
        if product_group_json != []:
            # product_dict_final['product_groups'] = get_product_group_stock(product_group_json)
            product_dict_final['groups_summary'] = get_product_group_stock_sum(
                product_group_json, product_json['configuration']['cdnUrl'])
        else:
            product_dict_final['groups_summary'] = []
        try:
            product_dict_final['product_attributes'] = get_product_attr(product_json['product']['attributes'])
        except:
            product_dict_final['product_attributes'] = []

    try:
        product_dict_final['other_merchants'] = {}
        for merchant in product_json['otherMerchants']:
            merchant_dict = {}
            merchant_dict['product_url'] = "https://www.trendyol.com" + \
                merchant['url']
            merchant_dict['product_price'] = merchant['price']
            merchant_product_json = get_details_raw_json(
                merchant_dict['product_url'])
            if merchant_product_json == 404:
                merchant_dict['product_variants'] = []
            merchant_dict['product_variants'] = get_product_variants(
                merchant_product_json)
    except KeyError:
        pass
    except Exception as exc:
        logger(exc, mode='exception')
    models_info_dict = {}
    for des in product_dict_final['content_descriptions']:
        des['description'].lower().replace("trendyol", "brandyto")
        if len(des['description'].lower().split('model dimensions')) != 1:
            try:
                dim_list = des['description'].lower().split('model dimensions')[
                    1].partition(":")[2].split('cm')
                for dim in dim_list:
                    dim_data = dim.split(":")
                    models_info_dict[dim_data[0]] = dim_data[1]
            except:
                models_info_dict['description'] = des['description']
    product_dict_final['models_info'] = models_info_dict

    product_dict_final['description_images'] = []
    try:
        img_sp = BeautifulSoup(product_json['htmlContent'], "html.parser")
        for each in img_sp.find_all("img"):
            product_dict_final['description_images'].append(
                each['data-src'].replace("{cdn_url}", product_json['configuration']['cdnUrl']))
    except:
        pass

    print(randint(1, 999),": Translating")
    import_product(tablename, product_dict_final)
    if TRANSLATE == True:
        for language in TRANS_LANGS:
            for each in langs_dict:
                if each == language:
                    translated_product = translate_product(product_dict_final, language, langs_dict[each])
                    import_product(f"{language}_{tablename}", translated_product)
    print("\n",randint(1, 999),": Imported product to db\r", end="")
    # try:
    #     #get_sim_cross.runner_func(product_dict_final['product_id'])
    # except KeyError:
    #     pass
    # Return Product details dictionary
    return 1
