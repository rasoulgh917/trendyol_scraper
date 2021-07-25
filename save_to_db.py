from db_tools import tables, engines
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json

def import_product(tablename, product_dict):
    try:
        product = tables.create(tablename)
        product.product_name = str(product_dict['product_name']).encode()
        product.product_images = str(product_dict['product_images']+product_dict['description_images']).encode()
        product.product_brand = str(product_dict['product_brand']).encode()
        product.product_category = str(product_dict['product_category']).encode()
        product.product_gender = str(product_dict['product_gender']).encode()
        product.product_price = str(product_dict['product_price']).encode()
        product.product_attributes = str(product_dict['product_attributes']).encode()
        product.content_descriptions = str(product_dict['content_descriptions']).encode()
        product.delivery_info = json.dumps(product_dict['delivery_info'])
        product.groups_summary = str(product_dict['groups_summary']).encode()
        product.product_seller_id = str(product_dict['product_seller']['id']).encode()
        product.product_seller_name = str(product_dict['product_seller']['name']).encode()
        product.product_seller_score = str(product_dict['product_seller']['sellerScore'])
        product.product_url = str(product_dict['product_url']).encode()
        product.product_variant = str(product_dict['variants']).encode()
        product.product_id = str(product_dict['product_id']).encode()
        product.stock_count = str(product_dict['variants'][0]['variant_stock_count']).encode()
        product.stock_status = str(product_dict['variants'][0]['variant_stock_status']).encode()
        Session = sessionmaker(bind=engines.engine)
        session = Session()
        session.add(product)
        session.commit()
    except Exception as exc:
        if exc == 'sellerScore':
            product.product_seller_score = None
    except IntegrityError:
        session.rollback()
    except:
        pass