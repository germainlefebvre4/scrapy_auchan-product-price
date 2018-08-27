# Scraper Auchan Product Price
Simple example of scraping a product price from Auchan Drive.

**Summary**
1. [Purpose](#purpose)
1. [Classes](#classes)
   1. [Attributes](#attributes)
   1. [Methods](#methods)
   1. [Functions](#functions)
      1. [List to String](#list-to-string-function)
      1. [String to Price](#string-to-price-function)
1. [Detailed sections](#)
   1. [Cookie persistence](#cookie-persistence)
   1. [Parse selector focus](#parse-selector-focus)

## Purpose

The initial purpose of this script was performing some tests about Scraping with scrapy framework. Finally it ended with successful results and make it usefull for explain a few concepts about scraping Scrapy Framework.

So purpose is now to parse a single product page, 1 product name with 1 product price on the whole page on Auchan Drive online store. This is a good example to try stuff and make you feel at ease with Scrapy.


## Class `ProductPriceSpider`

Single product page would load simple case to handle and goal is to catch Product name and price from web page.

Let's view some important sections about the Framework.

### Attributes

#### Class attributes
Scrapy Framework has some mandatory attributes to be filled to rollon. A good starting with good attribiutes would be these one :
* `name`: Name of the class in logs and traces,
* `start_urls`: URLs natively used in (first) `start_requests()` method,

#### User attributes
Out of the box you can define attributes that will be processed through Scrapy Framework. It helps to better understand what you are doing with your variables. User attributes are this one :
* `my_urls`: URLs user configured used for parsing.

### Methods

Scrapy starts with mandatory class in order to initiate the scrapy workflow. The only class method mandatory is `def start_requests(self)`. You can create user methods and chain them with starting `start_requests()` method.

#### Class methods
* `start_requests`: Start browsering and choose Auchan Drive Location.

#### User methods
* `product_page`: Browse product page,
* `parse`: Parse and retrieve product price.


### Functions

For factorizing reasons I chose to make 2 simple functions.
Don't worry it is only draft version. It makes us to reveal the lisibility conditions for the code.

### List to String function
Simply change list to string join list elements for `no-space` caracter.

Parameter:
* List

Returns:
* String

### String to Price function
Function that deletes non-price-caracters and returning a string of the price.

Parameter:
* String

Returns:
* String


## Detailed sections

This is some discovers found about how some stuff works and how to master them.

### Cookie persistence

In our case cookie is used to remain Shop Location so it must be preserve for all the browsering journey.
All we need is to keep the same value for the `cookiejar` meta attribute
```py
scrapy.Request(url, meta={'cookiejar': category}, callback=self.product_page)
```

You can see our chosen way in Python script `PriceScraper.py` :
```py
class ProductPriceSpider(scrapy.Spider):
    [...]

    start_urls = ['https://www.auchandrive.fr/drive/mag/Englos-924']
    my_urls = ['https://www.auchandrive.fr/catalog/coca-cola-zero-1l-P762493']

    def start_requests(self):
        # Start browsering and set the shop location in cookies with cookiejar="Englos"
        for url in self.start_urls:
            category = "Englos"
            yield scrapy.Request(url, meta={'cookiejar': category}, callback=self.product_page)

    def product_page(self, response):
        # Keep broswering and use the shop location in cookies with cookiejar="Englos"
        for url in self.my_urls:
            category = "Englos"
            yield scrapy.Request(url, meta={'cookiejar': category}, callback=self.parse)

    [...]
```

### Parse selector focus

Parsing is another step not necessary obvious for people beginning with `scrapy`.
You need to know that the following example run in a way :
* We start with find a recurrent HTML Block set by `SET_SELECTOR`. Here `class="pdp-buy"` defined by __CSS Selector Syntax__ `.pdp-buy`.
* We start processing the data selectors :
  * `PRICE_UNIT_SELECTOR` focused with __CSS Selector Syntax__ `div .price--per ::text`,
  * `PRICE_TOTAL_SELECTOR` focused with __CSS Selector Syntax__ `div .pdp-price span ::text`.

```py
    def parse(self, response):
        SET_SELECTOR = '.pdp-buy'
        for productprice in response.css(SET_SELECTOR):
            PRICE_UNIT_SELECTOR = 'div .price--per ::text'
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
```

To catch the focused data, I mean the product price, we use `css` function to make the selector `PRICE_TOTAL_SELECTOR` :
```py
PRICE_TOTAL_SELECTOR = 'div .pdp-price span ::text'
```
Then we can extract the first value occurence :
```py
productprice.css(PRICE_TOTAL_SELECTOR).extract_first()
```
or **our choice** all the included occurences returning a List :
```py
productprice.css(PRICE_TOTAL_SELECTOR).extract()
```

Another way to select the `PRICE_TOTAL_SELECTOR` would be to use `xpath` function to focus on. This is how we can handle our case with `xpath`way :
`PRICE_TOTAL_SELECTOR = '//p[@class="price-standard"]/span/text()'`

In further code processing we will use the `xpath` syntax because it is so much powerful compared to `css` syntax even if a bit harder to manage.
