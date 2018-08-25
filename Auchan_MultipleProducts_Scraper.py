#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re, json
import scrapy, requests as Request
import sys, io

# https://www.auchandrive.fr/drive/mag/Englos-924
# https://www.auchandrive.fr/recherche/coca

class ProductsSpider(scrapy.Spider):

    # User attributes
    # Store informations
    store_locations = [
        "https://www.auchandrive.fr/drive/mag/Englos-924",
        "https://www.auchandrive.fr/drive/mag/Villeneuve-dAscq-V2-823",
        "https://www.auchandrive.fr/drive/mag/Grasse-537",
    ]
    store_search = [
        "https://www.auchandrive.fr/catalog/coca-cola-zero-1l-P762493",
        "https://www.auchandrive.fr/recherche/coca",
    ]

    # Saving file informations
    file_path = "./"
    file_name = "auchan_products.json"
    file_json= {"Company": { "Name": "Auchan", "Location": {} } }


    # Class attributes
    name = 'products'
    start_urls = store_locations
    custom_settings = {
        #'DUPEFILTER_DEBUG': True,
    }



    def start_requests(self):

        # Save store location in cookies
        for url in self.start_urls:
            cookiejar = url.split('/')[-1].split('-')[:-1][0]
            print(cookiejar)
            self.file_json["Company"]["Location"][cookiejar] = {}
            self.file_json["Company"]["Location"][cookiejar]["Products"] = []
            yield scrapy.Request(url, meta={'cookiejar': cookiejar},
                                 dont_filter = True,
                                 callback=self.product_page)

    def product_page(self, response):
        # Browser product list page
        print(response.meta["cookiejar"])
        cookiejar = response.meta["cookiejar"]
        for url in self.store_search:
            if "/recherche/" in url:
                # Case search/multiple products
                yield scrapy.Request(url + "?startIndex=20",
                                     meta={'cookiejar': cookiejar},
                                     dont_filter = True,
                                     callback=self.parse_search)
            elif "/catalog/" in url:
                # Case single product
                yield scrapy.Request(url,
                                     meta={'cookiejar': cookiejar},
                                     dont_filter = True,
                                     callback=self.parse_product)

    def parse_search(self, response):
        # Parse product list page
        location = response.meta["cookiejar"]
        save_products = []

        SET_SELECTOR = '.product-item'
        for product in response.css(SET_SELECTOR):
            # Set selector xpath
            PRODUCT_NAME_SELECTOR = './/dt[@class="product-item__title"]/span/text()'
            PRODUCT_PRICE_SELECTOR = './/p[@class="price-standard"]/span/text()'
            PRODUCT_PRICEPER_SELECTOR = './/span[@class="product-item__price-per"]/text()'

			# Process data
            product_name = product.xpath(PRODUCT_NAME_SELECTOR).extract_first()
            product_price = "".join(product.xpath(PRODUCT_PRICE_SELECTOR).extract()).replace("\u20ac", "")
            product_priceper = re.sub(r" \u20ac.*", "", product.xpath(PRODUCT_PRICEPER_SELECTOR).extract_first())

            # Print data
            product_data = {
                'Name': product_name,
                'Price': product_price,
                'Priceper': product_priceper,
            }
            save_products.append(product_data)
        #print(product_data)
        self.save_file(location, save_products)

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

            # Print data
            product_data = {
                'Name': product_name,
                'Price': product_price,
                'Priceper': product_priceper,
            }
            save_products.append(product_data)
        #print(product_data)
        self.save_file(location, save_products)


    def save_file(self, location, save_products):
        #json_data = {"Company": { "Name": "Auchan", "Location": { "Name": location, "Products": save_products}}}
        #self.file_json["Company"]["Location"].append( { "Name": location, "Products": save_products } )
        self.file_json["Company"]["Location"][location]["Products"] += save_products

        # Save data in file
        #with open(self.file_path + self.file_name, "wb") as file:
        #  file.write(json.dumps(save_products, indent=2, ensure_ascii=False).encode('utf8'))
        #  file.close()

        #yield self.file_json
        with io.open(self.file_path + self.file_name, 'w', encoding='utf8') as file:
            json.dump(self.file_json, file, indent=2, ensure_ascii=False)
