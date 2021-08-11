from db_tools import engines
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column, VARCHAR, SmallInteger
from sqlalchemy.dialects.mysql import LONGTEXT

Base = declarative_base()

def import_product(tablename, product_dict):
    class Product(Base):
        __tablename__ = tablename
        id = Column(Integer, primary_key=True)
        product_name = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_images = Column(
            String(4294967295, collation='utf8mb4_general_ci'), nullable=True)
        product_brand = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_category = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_url = Column(
            LONGTEXT(collation='utf8mb4_general_ci'), nullable=True)
        product_id = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True, unique=True)
        product_attributes = Column(
            LONGTEXT(collation='utf8mb4_general_ci'), nullable=True)
        content_descriptions = Column(
            LONGTEXT(collation='utf8mb4_general_ci'), nullable=True)
        product_rating = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_price = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_gender = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_seller_id = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_seller_name = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_seller_score = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        stock_status = Column(
            VARCHAR(5, collation='utf8mb4_general_ci'), nullable=True)
        stock_count = Column(
            VARCHAR(5, collation='utf8mb4_general_ci'), nullable=True)
        delivery_info = Column(
            VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)
        product_variant = Column(
            LONGTEXT(collation='utf8mb4_general_ci'), nullable=True)
        groups_summary = Column(
            LONGTEXT(collation='utf8mb4_general_ci'), nullable=True)
    try:
        product = Product()
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
        # product.product_seller_score = str(product_dict['product_seller']['sellerScore'])
        product.product_seller_score = None
        product.product_url = str(product_dict['product_url']).encode()
        product.product_variant = str(product_dict['variants']).encode()
        product.product_id = str(product_dict['product_id']).encode()
        product.stock_count = str(product_dict['variants'][0]['variant_stock_count']).encode()
        product.stock_status = str(product_dict['variants'][0]['variant_stock_status']).encode()
        Session = sessionmaker(bind=engines.engine)
        session = Session()
        session.add(product)
        session.commit()
        session.close()

    except IntegrityError:
        session.rollback()
        session.close()