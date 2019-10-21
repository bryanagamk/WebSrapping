from flask_restful import Resource, reqparse
import logging as logger
import json
from .products_model import db, OProduct
import requests
import urllib.request
from bs4 import BeautifulSoup

# inisialisasi parameter yang akan diterima
parser = reqparse.RequestParser()
parser.add_argument('url', type=str)
parser.add_argument('id', type=int)
parser.add_argument('brand', type=str)
parser.add_argument('name', type=str)
parser.add_argument('price', type=int)

class Product(Resource):

    def post(self):
        # Ambil object parameter
        args = parser.parse_args()
        # Ambil parameter url
        '''
        contoh request user saat memberikan perintah mengambil data dari url yang diinginkan
        {
            "url": "https://www.sociolla.com/search?controller=search&orderby=position&orderway=desc&search_query=concealer&p=1",
        }
        '''
        url = str(args['url'])
        # setelah berhasil diambil, masukkan url tersebut ke fungsi get_product untuk scrapping data dari url tsb
        datas = get_product(url)
        print(datas)
        # setelah berhasil melakukan scrapping data-data yang kita butuhkan, simpan ke db
        for item in datas:
            item = OProduct(url=url, brand=item['brand'], name=item['name'], price=item['price'])
            db.session.add(item)
        db.session.commit()

        logger.debug("Inside the post method of Product")
        return {"message" : "Inside post method", "data" : datas},200

    def get(self):
        # mengambil semua data di tabel Product, melalui model OProduct, dan diurutkan ASC berdasarkan kolom price
        datas = OProduct.query.order_by(OProduct.price).all()
        # proses dibawah ini merubah data object SQLAlchemy menjadi list of dictionary(json) secara manual
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
        # mengambil object parameter
        args = parser.parse_args() 
        '''
        contoh request untuk merubah data dengan id : 12
        {
            "id": 12,
            "brand": "Test Put",
            "name": "Ganti nama",
            "price": 2500
        }
        '''
        # mengambil data product sesuai primary key dari request parameter id
        product = OProduct.query.get(args['id'])
        # update data product tsb dengan langsung mengassign data per-kolom
        product.brand = args['brand']
        product.name = args['name']
        product.price = args['price']
        
        # simpan perubahan data
        db.session.commit()

        # proses dibawah ini merubah data object SQLAlchemy menjadi list of dictionary(json) secara manual
        listproduct = []
        item = dict()
        item['id'] = product.id
        item['url'] = product.url
        item['brand'] = product.brand
        item['name'] = product.name
        item['price'] = product.price
        listproduct.append(item)

        logger.debug("Inside the put method of Product")
        return {"message" : "Inside put method and success update data", "data" : listproduct},200

    def delete(self):
        # mengambil object parameter
        args = parser.parse_args()
        # mengambil data sesuai primary key dari request parameter 'id'
        product = OProduct.query.get(args['id'])
        
        # hapus data yang sudah ditemukan
        db.session.delete(product)
        # simpan perubahan
        db.session.commit()

        logger.debug("Inside the delete method of Product")
        return {"message" : "Inside delete method and success delete data"},200

# fungsi untuk scrapping data
def get_product(url):
    response = requests.get(url)

    # inisialisasi obj BS4/ beautifulsoup
    soup = BeautifulSoup(response.text, "html.parser")
    # cari semua tag div dengan class product-item eec-data, karena data name, brand, price berada di dalam tag dan class tsb
    products_div = soup.find_all("div", "product-item eec-data")
    products = []
    # setelah mendapatkan semua tag dengan class tsb, cari secara spesifik data yang diinginkan
    for item in products_div:
        product = dict()
        # karena value yang diinginkan berada di tag <p> dengan class "text-center title", gunakan fungsi find untuk mencari data spesifik tsb
        name = item.find("p", "text-center title")
        price = item.find("p", "text-center price")
        # karena data brand berada di dalam tag, dan sebagai value dari sebuah class tag maka cara mengambilnya seperti mengmabil array atau dictionary  
        brand = item['data-eec-brand']

        # simpan pada variable local
        product['brand'] = brand
        product['name'] = name.text
        # simpan dan rubah data string price ke int 
        product['price'] = int(price.text[3:].replace(".",""))
        products.append(product) 
    return products