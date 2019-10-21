import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = "https://www.sociolla.com/search?controller=search&orderby=position&orderway=desc&search_query=concealer&p=1"
response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")
products = soup.find_all("div", "product-item eec-data")

names = []
prices = []
brands = []
products_dict = []
print(url)
for item in products:
    product_dict = dict()
    # print what you find
    name = item.find("p", "text-center title")
    price = item.find("p", "text-center price")
    brand = item['data-eec-brand'] 

    product_dict['name'] = name.text
    product_dict['price'] = price.text
    products_dict.append(dict(product_dict))

print(products_dict)

