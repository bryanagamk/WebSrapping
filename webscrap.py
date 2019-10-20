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
print(url)
for item in products:
    # print what you find
    print("\n")
    name = item.find("p", "text-center title")
    print(name)
    price = item.find("p", "text-center price")
    print("\n")
    print(price)
    brand = item['data-eec-brand'] 
    print("\n")
    print(brand)
    # Store to variable
    names.append(name)
    prices.append(price)
    brands.append(brand)
