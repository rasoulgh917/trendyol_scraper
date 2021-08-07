from bs4 import BeautifulSoup
import requests as req
import requests_cache
import json
import sys
from urllib.parse import urlparse, urlunparse
from translate import translator
from logger import logger

requests_cache.install_cache('cache', 'sqlite', 120)

def get_offers_cats():
    # Connect to trendyol
    try:
        trendyol_ = req.get('https://www.trendyol.com/')
    except:
        logger("Failed to connect to trendyol for offers, retrying ...")
        trendyol_ = req.get('https://www.trendyol.com/')

    # Load HTML
    soup = BeautifulSoup(trendyol_.text, 'html.parser')

    # Extract Data
    categories = soup.find_all('li', {'class': 'tab-link'})
    cat_dict = {}

    # Maintain Links and Translate data
    for cat in categories:
        url_parts = list(urlparse(cat.a['href']))
        url_parts[0] = 'https'
        url_parts[1] = 'www.trendyol.com'
        url = urlunparse(url_parts)
        name_translated = translator(cat.a.contents[0])
        cat_dict[name_translated] = url

    return cat_dict


def list_offers(category_link):
    # Connect to trendyol
    try:
        trendyol = req.get(category_link)
    except:
        logger("Failed to connect to trendyol for offers, retrying ...")
        trendyol = req.get(category_link)

    # Load HTML
    soup = BeautifulSoup(trendyol.text, 'html.parser')

    # Extract Data
    offers_div = soup.find('div', {'class': 'sticky-wrapper'})
    offers_list = offers_div.find_all('article')
    offers = {}

    # Maintain links and translate data
    for link in offers_list:
        url_parts = list(urlparse(link.a['href']))
        url_parts[0] = 'https'
        url_parts[1] = 'www.trendyol.com'
        url = urlunparse(url_parts)
        name_translated = translator(link.a.summary.span.contents[0])
        offers[name_translated] = url

    return offers
