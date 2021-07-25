from translate import translator
from config import TRANSLATE, TRANS_LANGS
from logger_ import logger
from random import randint
import asyncio
from save_to_db import import_product

def translate_product(product_dict, dest, tablename):
    product_dict['product_name'] = translator(
        product_dict['product_name'], dest)
    product_dict['product_category'] = translator(
        product_dict['product_category'], dest)
    if product_dict != []:
        product_dict['product_gender'] = translator(
            product_dict['product_gender'], dest)
        for each in product_dict['variants']:
            each['variant_name'] = translator(
                each['variant_name'], dest)
            if not len(each['variant_value']) in [1, 2, 3]:
                each['variant_value'] = translator(
                    each['variant_value'], dest)
    for each in product_dict['content_descriptions']:
        each['description'] = translator(
            each['description'], dest)
    if product_dict['product_attributes'] != []:
        for each in product_dict['product_attributes']:
            each['key'] = translator(
                each['key'], dest)
            each['value'] = translator(
                each['value'][0], dest)
    if product_dict['groups_summary'] != []:
        for group in product_dict['groups_summary']:
            for attr in group['attributes']:
                try:
                    attr['attribute_name'] = translator(attr['attribute_name'], dest)
                except KeyError:
                    pass
                for var in attr['attribute_variants']:
                    var['variant_name'] = translator(var['variant_name'], dest)
                attr['product_name'] = translator(attr['product_name'], dest)

    import_product(f"{dest}_{tablename}", product_dict)


def translate_call(product_dict, tablename):
    if TRANSLATE == True:
        for language in TRANS_LANGS:
            translate_product(product_dict, language, tablename)
    import_product(tablename, product_dict)