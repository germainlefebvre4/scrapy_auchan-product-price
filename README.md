# Scraper Auchan Product Price
Simple example of scraping a product price from Auchan Drive.

**Summary**
1. [Context and dependencies](#context-and-dependencies)
1. [Running the scrap](#running-the-scrap)
1. [Workflow](#workflow)
1. [Classes](#classes)
   1. [Attributes](#attributes)
   1. [Methods](#methods)
1. [Functions](#functions)
   1. [List to String](#list-to-string-function)
   1. [String to Price](#string-to-price-function)
1. [Detailed sections](#)
   1. [Cookie persistence](#cookie-persistence)
   1. [Parse selector focus](#parse-selector-focus)


## Context and dependencies

Code run from Visual Studio Code 2017 with Python and C++ environements configured.
Python version selected is `python-3.6` because of dependencies with scrapy package (not compatible with python-3.7 yet).

Python dependencies and versions :
* `pywin32-223`
* `requests-2.19.1`
* `scrapy-1.5.1`


## Running the scrap

Scrapy has its own libraries running without including all you need. With this behaviour you just need to focus on **scrapping** your data.

Running a scrapy job written in `PriceScraper.py` :
```py
scrapy runspider PriceScraper.py
```


## Workflow

If you directly browse product you can see that you are directly redirected to an error page `page_non_trouvee.html`.

You need to first select a Drive Location before browsing product. We chose to go at [Auchan Drive Englos](#https://www.auchandrive.fr/drive/mag/Englos-924).

Thus we can show product informations. We chose product [Coca-Cola Zero 1L](#https://www.auchandrive.fr/catalog/coca-cola-zero-1l-P762493).


## Class `ProductPriceSpider`

### Attributes

Class attributes:
* `name`: Name of the class in logs and traces,
* `start_urls`: URLs natively used in (first) `start_requests()` method,
* `my_urls`: URLs user configured used for parsing.

### Methods

Class methods:
* `start_requests`: Start browsering and choose Auchan Drive Location,
* `product_page`: Browse product page,
* `parse`: Parse and retrieve product price.


## Functions

For factorizing reasons I chose to make 2 simple functions.

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
* We start at HTML Block set by `SET_SELECTOR`. Here `class="pdp-buy"` defined by __CSS Selector Syntax__ `.pdp-buy`.
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
`PRICE_TOTAL_SELECTOR = '//p[@class="price-standard"]/span/text()'
```
Then we
