import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = "https://www.sociolla.com/search?controller=search&orderby=position&orderway=desc&search_query=concealer&p=1"
response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")
products = soup.find_all("div", "product-item")

names = []
prices = []
for item in products:
    name = item.find("p", "text-center title")
    price = item.find("p", "text-center price")
    names.append(name)
    prices.append(price)

print(url)
for i, n in enumerate(names):
    print(names[i].text)
    print("\n")
    print(prices[i].text)
    print("\n")    
