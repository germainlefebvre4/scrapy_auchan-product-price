import logging
import re
import scrapy, requests as Request

# Navigation Journey
# https://www.auchandrive.fr/drive/mag/Englos-924
# https://www.auchandrive.fr/catalog/coca-cola-zero-1l-P762493

class ProductPriceSpider(scrapy.Spider):

    name = 'productprice'
    start_urls = ['https://www.auchandrive.fr/drive/mag/Englos-924']
    my_urls = ['https://www.auchandrive.fr/catalog/coca-cola-zero-1l-P762493']


    def start_requests(self):
        for url in self.start_urls:
            #category = url.split('/')[-1]
            category = "Englos"
            yield scrapy.Request(url, meta={'cookiejar': category}, callback=self.product_page)

    def product_page(self, response):
        for url in self.my_urls:
            category = "Englos"
            yield scrapy.Request(url, meta={'cookiejar': category}, callback=self.parse)


    def parse(self, response):
        SET_SELECTOR = '.pdp-buy'
        for productprice in response.css(SET_SELECTOR):
            PRICE_UNIT_SELECTOR = 'div .price--per ::text'
            #PRICE_TOTAL_SELECTOR = '//p[@class="price-standard"]/span/text()' # xpath
            PRICE_TOTAL_SELECTOR = 'div .pdp-price span ::text' # css
            yield {
                'Price Unit': string_to_price(
                    productprice.css(PRICE_UNIT_SELECTOR).extract_first()
                    ),
                'Price Total': string_to_price(
                    list_to_string(
                        productprice.css(PRICE_TOTAL_SELECTOR).extract()
                        )
                    ),
            }

def list_to_string(list_price):
        return "".join(list_price)

def string_to_price(str_price):
        return re.sub(r"[^\d|,]", "", str_price)
