# Scraper Auchan Multiple Products
Complete example of scraping products price from Auchan Drive coming from either single product or search results.

**Summary**
1. [Purpose](#purpose)
1. [Classes](#classes)
   1. [Attributes](#attributes)
   1. [Methods](#methods)
1. [Detailed sections](#)
   1. [Cookie persistence](#cookie-persistence)
   1. [Parse selector focus](#parse-selector-focus)

## Context and dependencies

Python dependencies:
* `requests`
* `scrapy`
* `pymongo`

## Purpose

## Class `ProductsSpider`

### Attributes

#### Class attributes
* `name`: Name of the class in logs and traces,
* `start_urls`: URLs natively used in (first) `start_requests()` method,
* `custom_settings`: Allow to override some 'system' value (internal framework configurations).

#### User attributes
Store attibutes:
* `store_locations`: (list) Store locations reprensented by the URL given when cliking on the button "Enter in this Drive";
* `store_search`: (list) Product page represented by 

### Methods

Class methods:
* `start_requests`: Start browsering and choose Auchan Drive Location,
* `product_page`: Browse product page,
* `parse_product`: Parse and retrieve product price from product page,
* `save_mongo`: Add data in JSON file then save it.


## Detailed sections

### Manipulate strings with `€` symbol

We encountered some difficulties to apprehend string manipulation for Euro symbol. Its manipulation differs from Dolar `$` manipulation so make feel buzzy.
We finally found a hard way to replace our strong caracter. On a lower level letters are converted in a ascci caracter and then processed. Keeping this way but converting it in hexadecimal makes much larger possibilities about encoding. So do we the symbol Euro `€` has a HEX UNICODE code equal to `\u20ac`.

Python function `replace()` will finnish th job for us.

```py
priceWithoutEuro = priceWithEuro.replace("\u20ac", "")
```

__Beware for using `python2`which recommands to handle in a different way symbols issue__
Prince handling `2,02€`:
```py
product_price = "".join(product.xpath(PRODUCT_PRICE_SELECTOR).extract()[:-1])
```

Price per handling `8,08 €/L`:
```py
product_priceper = product.xpath(PRODUCT_PRICEPER_SELECTOR).extract_first().split(" ")[0]
```
