from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)

base = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db

db = SQLAlchemy(app)

# init marshmallow

ma = Marshmallow(app)

# product class/model

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quant = db.Column(db.Integer)

    def __init__(self, name, description, price, quant):
        self.name = name
        self.description = description
        self.price = price
        self.quant = quant


# product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quant')


# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#create a product

@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quant = request.json['quant']

    new_product = Product(name, description, price, quant)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route('/product', methods=['GET'])
def get_products():
    all = Product.query.all()
    result = products_schema.dump(all)
    return jsonify(result)

@app.route('/product/<id>', methods=['GET'])
def get_product(id  ):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['PUT'])
def update_produt(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quant = request.json['quant']

    product.name = name
    product.decription = description
    product.price = price
    product.quant = quant

    db.session.commit()

    return product_schema.jsonify(product)



@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    
    return product_schema.jsonify(product)

    

# run server
if __name__ == "__main__":
    app.run(debug=True)