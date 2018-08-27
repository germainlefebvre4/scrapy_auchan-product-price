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

## Purpose

## Class `ProductsSpider`

### Attributes

#### Class attributes
* `name`: Name of the class in logs and traces,
* `start_urls`: URLs natively used in (first) `start_requests()` method,
* `custom_settings`: Allow to override some 'system' value (internal framework configurations).

#### User attributes
Store attibutes :
* `store_locations`: (list) Store locations reprensented by the URL given when cliking on the button "Enter in this Drive";
* `store_search`: (list) Product page represented by 

File attributes for data storage after scraping in JSON format :
* `file_path`: (string) Path of the file,
* `file_name`: (string) Name of the file,
* `file_json`: (string) Initial structure for the JSON file.

### Methods

Class methods:
* `start_requests`: Start browsering and choose Auchan Drive Location,
* `product_page`: Browse product page,
* `parse_search`: Parse and retrieve products price from search
* `parse_product`: Parse and retrieve product price from product page,
* `save_file`: Add data in JSON file then save it.


## Detailed sections

### Manipulate strings with `€` symbol

We encountered some difficulties to apprehend string manipulation for Euro symbol. Its manipulation differs from Dolar `$` manipulation so make feel buzzy.
We finally found a hard way to replace our strong caracter. On a lower level letters are converted in a ascci caracter and then processed. Keeping this way but converting it in hexadecimal makes much larger possibilities about encoding. So do we the symbol Euro `€` has a HEX UNICODE code equal to `\u20ac`.

Python function `replace()` will finnish th job for us.

```py
priceWithoutEuro = priceWithEuro.replace("\u20ac", "")
```


### Save file

We encountered a subtility at saving JSON data in JSON file : encoding. It is quite a mess when you start managing data encoding from different librairies for different prupose.

We started to save data with native built-in function `open()`. We quickly got some weird print for special caracters like accentued one. Hard to handle on first sight but we did it !

```py
def save_file(self, ...):
    with open(self.file_path + self.file_name, "wb") as file:
        file.write(json.dumps(save_products, indent=2, ensure_ascii=False).encode('utf8'))
        file.close()
```

And we found another way to save data in a JSON structure with the python librairy `io`. The way is quite similar but allow more flexible usage. A nice `import io` will allow you to use `io.open()`.

```py
def save_file(self, ...):
    with io.open(self.file_path + self.file_name, 'w', encoding='utf8') as file:
        json.dump( { "Name": "Auchan", "Locations": [] } , file, indent=2, ensure_ascii=False)
```
