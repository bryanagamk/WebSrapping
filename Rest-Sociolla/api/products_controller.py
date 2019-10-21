from flask_restful import Resource, reqparse
import logging as logger
import json
from .products_model import db, OProduct
import requests
import urllib.request
from bs4 import BeautifulSoup

parser = reqparse.RequestParser()
parser.add_argument('url', type=str)

class Product(Resource):

    def post(self):
        args = parser.parse_args()
        url = str(args['url'])
        datas = get_product(url)
        print(datas)
        for item in datas:
            item = OProduct(url=url, brand=item['brand'], name=item['name'], price=item['price'])
            db.session.add(item)
        db.session.commit()

        logger.debug("Inside the post method of Product")
        return {"message" : "Inside post method", "data" : datas},200

    def get(self):
        datas = OProduct.query.order_by(OProduct.price).all()
        listproduct = []
        for data in datas:
            item = dict()
            item['id'] = data.id
            item['brand'] = data.brand
            item['name'] = data.name
            item['price'] = data.price
            listproduct.append(item)

        return {"message" : "Inside get method of Product", "data" : listproduct},200

    def put(self):
        logger.debug("Inside the put method of Product")
        return {"message" : "Inside put method"},200

    def delete(self):
        logger.debug("Inside the delete method of Product")
        return {"message" : "Inside delete method"},200

def get_product(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    products_div = soup.find_all("div", "product-item eec-data")
    products = []
    for item in products_div:
        product = dict()
        name = item.find("p", "text-center title")
        price = item.find("p", "text-center price")
        brand = item['data-eec-brand']

        product['brand'] = brand
        product['name'] = name.text
        product['price'] = int(price.text[3:].replace(".",""))
        products.append(product) 
    return products