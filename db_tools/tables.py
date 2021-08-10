from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column, VARCHAR, SmallInteger
from sqlalchemy.dialects.mysql import LONGTEXT
from .config import *
from .engines import engine

Base = declarative_base()

def create(tablename):
    Base.metadata.clear()
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
        # table_name_form = Column(
        #     VARCHAR(255, collation='utf8mb4_general_ci'), nullable=True)

    return Product()



class Checker(Base):
    __tablename__ = CHECKER_TABLE_NAME

    id = Column(Integer, primary_key=True)
    name = Column(
        String(4294967295, collation='utf8mb4_general_ci'), nullable=True)