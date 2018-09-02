#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import scrapy, requests as Request
import pymongo
from pymongo import MongoClient

# https://www.auchandrive.fr/drive/mag/Englos-924
# https://www.auchandrive.fr/recherche/coca

class ProductsSpider(scrapy.Spider):

    # User attributes
    # Store informations
    store_locations = [
        "https://www.auchandrive.fr/drive/mag/Englos-924",
        "https://www.auchandrive.fr/drive/mag/Faches-Thumesnil-361",
    ]
    store_search = [
        "https://www.auchandrive.fr/catalog/jardin-bio-pur-jus-de-citron-vert-25cl-P513766",
    ]

    # Class attributes
    name = 'products'
    start_urls = store_locations


    def start_requests(self):
        # Save store location in cookies
        for url in self.start_urls:
            cookiejar = url.split('/')[-1].split('-')[:-1][0]
            yield scrapy.Request(url, meta={'cookiejar': cookiejar},
                                 dont_filter = True,
                                 callback=self.product_page)


    def product_page(self, response):
        # Browser product list page
        cookiejar = response.meta["cookiejar"]
        for url in self.store_search:
            # Case single product
            yield scrapy.Request(url,
                                 meta={'cookiejar': cookiejar},
                                 dont_filter = True,
                                 callback=self.parse_product)


    def parse_product(self, response):
        # Parse product list page
        location = response.meta["cookiejar"]
        save_products = []

        SET_SELECTOR = '.pdp-infos'
        for product in response.css(SET_SELECTOR):
            # Set selector xpath
            PRODUCT_NAME_SELECTOR = './/p[@class="pdp-infos__title"]/text()'
            PRODUCT_PRICE_SELECTOR = './/p[@class="price-standard"]/span/text()'
            PRODUCT_PRICEPER_SELECTOR = './/p[@class="price--per"]/text()'

			# Process data
            product_name = re.sub(r"(\n *)", "", product.xpath(PRODUCT_NAME_SELECTOR).extract_first())
            product_price = "".join(product.xpath(PRODUCT_PRICE_SELECTOR).extract()).replace("\u20ac", "")
            product_priceper = re.sub(r" \u20ac.*", "", product.xpath(PRODUCT_PRICEPER_SELECTOR).extract_first())

            # Format data
            mongo_data = {
                'Company': 'Auchan',
                'Location': location,
                'Product': product_name,
                'Price': product_price,
                'Priceper': product_priceper,
            }

            self.save_mongo(mongo_data)
        

    def save_mongo(self, product_data):
        # Save products in Mondo Database
        # Here is a dev/test database
        client = MongoClient("ds141872.mlab.com", 41872)
        db = client['auchan-products']
        db.authenticate("scrapy59", "scrapy59")
        collection = db['products']

        query_filter = product_data.copy()
        for key in set(product_data.keys()) - set(["Company", "Location", "Product"]):
            del query_filter[key]

        if collection.find(query_filter).count() > 0:
            collection.replace_one(query_filter, product_data)
        else:
            collection.insert(product_data)