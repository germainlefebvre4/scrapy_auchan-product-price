# How to scrap products from Auchan Drive websites

You can find mindset and examples for scraping a product pricse from Auchan Drive websites.

It is tidied by project shots that have single of multiple purposes.

**Summary**
1. [Context and dependencies](#context-and-dependencies)
1. [Running the scrap](#running-the-scrap)
1. [Workflow](#workflow)
1. [Goal of directories and projects](#goal-of-directories-and-projects)



## Context and dependencies

Code run from Visual Studio Code 2017 with Python and C++ environements configured.
Python version selected is `python-3.6` because of dependencies with scrapy package (not compatible with `python-3.7` yet).

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


## Goal of directories and projects

Sens and goal of directories:
* SingleProductParser: Quick simple example to focus on Scrapy Framework,
* MultipleProductsParser: Script to parse prices from multiple sources of products (product page and search page),
* ProductsSaveMongo: Evolved version with better structured data and saving into a MongoDB,

