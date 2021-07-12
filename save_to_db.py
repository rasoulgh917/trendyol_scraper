from db_tools import tables, engines
from sqlalchemy.orm import sessionmaker

def import_product(tablename, product_dict):
    product = tables.create_product(tablename)
    product.product_name = product_dict['product_name']
    product.product_images = product_dict['product_images']
    product.product_brand = product_dict['product_brand']
    product.product_category = product_dict['product_category']
    product.product_gender = product_dict['product_gender']
    product.product_price = product_dict['product_price']
    product.product_attributes = product_dict['product_attributes']
    product.content_descriptions = product_dict['content_descriptions']
    product.delivery_info = product_dict['delivery_info']
    product.groups_summary = product_dict['groups_summary']
    product.product_seller_id = product_dict['product_seller']['id']
    product.product_seller_name = product_dict['product_seller']['name']
    product.product_seller_score = product_dict['product_seller']['sellerScoreColor']
    product.product_url = product_dict['product_url']
    product.product_variant = product_dict['variants']
    product.product_id = product_dict['product_id']
    product.stock_count = product_dict['variants'][0]['variant_stock_count']
    product.stock_status = product_dict['variants'][0]['variant_stock_status']
    Session = sessionmaker(bind=engines.engine)
    session = Session()
    session.add(product)
    session.commit()