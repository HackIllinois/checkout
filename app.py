import os
from flask import Flask, jsonify, request
from models import db, Item, Hacker
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/api/all_items', methods=['GET'])
def all_items():
    item_list = []
    items = Item.query.all()
    for item in items:
        new_item = {}
        new_item['id'] = item.id
        new_item['name'] = item.name
        new_item['description'] = item.description
        new_item['barcode'] = item.barcode
        item_list.append(new_item)
    return jsonify(items=item_list)

@app.route('/api/new_item', methods=['POST'])
def new_item():
    name = request.form['name']
    description = request.form['description']
    barcode = request.form['barcode']
    item = Item(name, description, barcode)
    db.session.add(item)
    db.session.commit()
    item_json = {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'barcode': item.barcode
                }
    return jsonify(item_json)

@app.route('/api/overview', methods=['GET'])
def overview():
    item_list = []
    items = Item.query.all()
    for item in items:
        new_item = {}
        new_item['id'] = item.id
        new_item['name'] = item.name
        new_item['description'] = item.description
        new_item['barcode'] = item.barcode
        item_list.append(new_item)
    return jsonify(items=item_list)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db.init_app(app)
    app.run(host='0.0.0.0', port=port, debug=True)