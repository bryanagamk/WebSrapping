from app import db

class OProduct(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200),)
    brand = db.Column(db.String(100),)
    name = db.Column(db.String(100),)
    price = db.Column(db.Integer,)

    def __repr__(self):
        return "id: {} url: {} brand: {} name: {} price: {}".format(self.id, self.url, self.brand, self.name, self.price)
