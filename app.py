import os
from flask import Flask, abort, jsonify, request
from models import db, Item, Hacker
from flask.ext.sqlalchemy import SQLAlchemy

from config import SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/items', methods=['GET'])
def all_items():
    items = Item.query.all()
    items_json = []
    for item in items:
        new_item = dict()
        new_item['name'] = item.name
        new_item['description'] = item.description
        new_item['quantity_left'] = item.quantity_left
        items_json.append(new_item)
    return jsonify(items=items_json)

@app.route('/hacker/<int:hacker_barcode>', methods=['GET'])
def hacker_items():
    hacker = Hacker.query.filter_by(barcode=hacker_barcode).first()
    hacker_json = {
        'id': hacker.id,
        'barcode': hacker.barcode,
        'items_checked_out': hacker.items_checked_out
    }
    return jsonify(hacker_json)

@app.route('/items/new', methods=['POST'])
def new_item():
    secret = request.form['secret']
    if secret != SECRET_KEY:
        return abort(403)

    name = request.form['name']
    description = request.form['description']
    quantity_left = request.form['quantity_left']
    item_barcodes = request.form['item_barcodes']
    item = Item(name, description, quantity_left, item_barcodes)
    db.session.add(item)
    db.session.commit()
    item_json = {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'quantity_left': item.quantity_left,
        'item_barcodes': item.item_barcodes
    }
    return jsonify(item_json)

@app.route('/items/checkout', methods=['POST'])
def checkout_item():
    secret = request.form['secret']
    if secret != SECRET_KEY:
        return abort(403)

    item_barcode = request.form['item_barcode']
    hacker_barcode = request.form['hacker_barcode']

    selected_item = (item for item in Items.query.all() if item_barcode in item.item_barcodes)
    selected_item.quantity_left -= 1

    hacker = Hacker.query.filter_by(barcode=hacker_barcode).first()
    if hacker:
        hacker.items_checked_out += ',' + item_barcode
    else:
        hacker = Hacker(hacker_barcode, item_barcode)
        db.session.add(hacker)
    db.session.commit()

    ret_json = []
    hacker_json = {
        'id': hacker.id,
        'barcode': hacker.barcode,
        'items_checked_out': hacker.items_checked_out
    }
    item_json = {
        'id': selected_item.id,
        'name': selected_item.name,
        'description': selected_item.description,
        'quantity_left': selected_item.quantity_left,
        'item_barcodes': selected_item.item_barcodes
    }
    ret_json.append(hacker_json)
    ret_json.append(item_json)
    return jsonify(info=ret_json)

@app.route('/items/return', methods=['POST'])
def return_item():
    secret = request.form['secret']
    if secret != SECRET_KEY:
        return abort(403)

    item_barcode = request.form['item_barcode']
    hacker_barcode = request.form['hacker_barcode']

    selected_item = (item for item in Items.query.all() if item_barcode in item.item_barcodes)
    selected_item.quantity_left += 1

    hacker = Hacker.query.filter_by(barcode=hacker_barcode).first()
    if hacker:
        hacker.items_checked_out.replace(item_barcode + ',', '')
    db.session.commit()

    hacker_json = {
        'id': hacker.id,
        'barcode': hacker.barcode,
        'items_checked_out': hacker.items_checked_out
    }
    return jsonify(hacker_json)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db.init_app(app)
    app.run(host='0.0.0.0', port=port, debug=True)
