from flask_restful import Api
from app import app
from .products_controller import Product

restServerInstance = Api(app)

restServerInstance.add_resource(Product,"/api/products")