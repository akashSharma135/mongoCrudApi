from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')

# creating database
db = client['productsDB']

app = Flask(__name__)


""" Get or Add product """
@app.route('/products', methods=['GET', 'POST'])
def get_or_add_product():
    if request.method == 'POST':
        product_details = request.get_json()
        
        product_name = product_details.get('product_name')
        product_desc = product_details.get('product_desc')
        product_quantity = product_details.get('product_quantity')
        product_price = product_details.get('product_price')
        
        
        # Inserting the new product
        db.product.insert_one({
            "product_name": product_name,
            "product_desc": product_desc,
            "product_quantity": product_quantity,
            "product_price": product_price
        })

        return jsonify({
            "message": "product added"
        }), 200
    
    products_list = []
    
    for product in db.product.find():
        products_list.append({
            "product_id": str(product['_id']),
            "product_name": product['product_name'],
            "product_desc": product['product_desc'],
            "product_quantity": product['product_quantity'],
            "product_price": product['product_price']
        })
    return jsonify(products_list), 200


""" Get product by id """
@app.route('/products/<id>')
def get_product_by_id(id):
    product = db.product.find_one({"_id": ObjectId(id)})
    
    if product:
        product_details = {
        "product_name": product['product_name'],
        "product_desc": product['product_desc'],
        "product_quantity": product['product_quantity'],
        "product_price": product['product_price']
        }
    
        return product_details, 200


""" Delete product by id """
@app.route('/products/delete/<id>', methods=['DELETE'])
def delete_product_by_id(id):
    if db.product.find_one({"_id": ObjectId(id)}):
        db.product.delete_one({"_id": ObjectId(id)})
        
        return jsonify({
            "message": f"product deleted! ID: {id}"
        })
    
    return jsonify({
        "message": "Product not found"
    }), 204
    
    
""" Update product """
@app.route('/products/update/<id>', methods=['PUT'])
def update_product_by_id(id):
    if db.product.find_one({"_id": ObjectId(id)}):
        product_details = request.get_json()
        db.product.update_one({"_id": ObjectId(id)}, {'$set':{"product_name": product_details['product_name'], "product_desc": product_details['product_desc'], "product_quantity": product_details['product_quantity'], "product_price": product_details['product_price']}})
        
        return jsonify({
            "message": "product updated"
        })
        
    return jsonify({
        "message": f"product doesn't exists of id: {id}"
    }), 204
       

if __name__ == '__main__':
    app.run(debug=True)