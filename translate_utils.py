from translate import translator
from config import TRANSLATE
from logger_ import logger
from random import randint

async def translate_product(product_dict):
    print(randint(1, 999),": Translating")
    trans_dict_dest = {}
    trans_dict_src = {}
    if TRANSLATE == True:
        trans_dict_src['product_name'] = product_dict['product_name']
        product_dict['product_name'] = translator(
            product_dict['product_name'])
        trans_dict_dest['product_name'] = product_dict['product_name']
        trans_dict_src['product_category'] = product_dict['product_category']
        product_dict['product_category'] = translator(
            product_dict['product_category'])
        trans_dict_dest['product_category'] = product_dict['product_category']
        if product_dict != []:
            product_dict['product_gender'] = translator(
                product_dict['product_gender'])
            for each in product_dict['variants']:
                each['variant_name'] = translator(
                    each['variant_name'])
                if not len(each['variant_value']) in [1, 2, 3]:
                    each['variant_value'] = translator(
                        each['variant_value'])
        trans_dict_src['content_descriptions'] = product_dict['content_descriptions']
        for each in product_dict['content_descriptions']:
            each['description'] = translator(
                each['description'])
        trans_dict_dest['content_descriptions'] = product_dict['content_descriptions']
        trans_dict_src['product_attributes'] = product_dict['product_attributes']
        if product_dict['product_attributes'] != []:
            for each in product_dict['product_attributes']:
                each['key'] = translator(
                    each['key'])
                each['value'] = translator(
                    each['value'][0])
        trans_dict_dest['product_attributes'] = product_dict['product_attributes']
        if product_dict['groups_summary'] != []:
            for group in product_dict['groups_summary']:
                for attr in group['attributes']:
                    try:
                        attr['attribute_name'] = translator(attr['attribute_name'])
                    except KeyError:
                        pass
                    for var in attr['attribute_variants']:
                        var['variant_name'] = translator(var['variant_name'])
                    attr['product_name'] = translator(attr['product_name'])
    print("Translation done")
    return [product_dict, trans_dict_dest, trans_dict_src]