from db_tools import tables, engines
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json

def import_product(tablename, product_dict):
    # try:
    product = tables.create(tablename)
    product.product_name = str(product_dict['product_name'])
    product.product_images = str(product_dict['product_images']+product_dict['description_images'])
    product.product_brand = str(product_dict['product_brand'])
    product.product_category = str(product_dict['product_category'])
    product.product_gender = str(product_dict['product_gender'])
    product.product_price = str(product_dict['product_price'])
    product.product_attributes = str(product_dict['product_attributes'])
    product.content_descriptions = str(product_dict['content_descriptions'])
    product.delivery_info = json.dumps(product_dict['delivery_info'])
    product.groups_summary = str(product_dict['groups_summary'])
    product.product_seller_id = str(product_dict['product_seller']['id'])
    product.product_seller_name = str(product_dict['product_seller']['name'])
    # product.product_seller_score = str(product_dict['product_seller']['sellerScore'])
    product.product_seller_score = None
    product.product_url = str(product_dict['product_url'])
    product.product_variant = str(product_dict['variants'])
    product.product_id = str(product_dict['product_id'])
    product.stock_count = str(product_dict['variants'][0]['variant_stock_count'])
    product.stock_status = str(product_dict['variants'][0]['variant_stock_status'])
    Session = sessionmaker(bind=engines.engine)
    session = Session()
    session.add(product)
    session.commit()
    # except Exception as exc:
    #     if exc == 'sellerScore':
    #         product.product_seller_score = None
    # except IntegrityError:
    #     session.rollback()