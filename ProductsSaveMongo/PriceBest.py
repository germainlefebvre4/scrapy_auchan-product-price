#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
#import yaml

#def load_config():
#    with open("config.yml", 'r') as ymlfile:
#        cfg = yaml.load(ymlfile)

#def mongo(db_addree=None, db_port=None, db_database=None, db_collection=None, db_username=None, db_password=None):
#    client = MongoClient(db_address, db_port)
#    db = client[db_database]
#    db.authenticate(db_username, db_password)
#    return db[db_collection]


if __name__ == "__main__":
    db_products_client = MongoClient("ds141872.mlab.com", 41872)
    db_products_db = mongo_products_client['auchan-products']
    db_products_db.authenticate("scrapy59", "scrapy59")
    db_products = mongo_products_db['products']

    bestPriceProduct = products.find_one(sort=[('Price', 1)])
    print("%s %s" % (bestPriceProduct["Product"], bestPriceProduct["Price"]))
