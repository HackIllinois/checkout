import os
from flask import Flask, abort, jsonify, request
from models import db, Item, Hacker
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from config import SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
	f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/items', methods=['GET'])
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def hacker_items(hacker_barcode):
    hacker = Hacker.query.filter_by(barcode=hacker_barcode).first()
    if not hacker:
        return abort(404)

    hacker_json = {
        'id': hacker.id,
        'barcode': hacker.barcode,
        'items_checked_out': hacker.items_checked_out
    }
    return jsonify(hacker_json)

@app.route('/items/new', methods=['POST'])
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def checkout_item():
    secret = request.form['secret']
    if secret != SECRET_KEY:
        return abort(403)

    item_barcode = request.form['item_barcode']
    hacker_barcode = request.form['hacker_barcode']

    selected_item = None
    for item in Item.query.all():
        if item_barcode in item.item_barcodes:
            selected_item = item
    if not selected_item:
        abort(404)
    selected_item.quantity_left -= 1

    hacker = Hacker.query.filter_by(barcode=hacker_barcode).first()
    if hacker:
        hacker.items_checked_out = hacker.items_checked_out + item_barcode + ','
    else:
        hacker = Hacker(hacker_barcode, item_barcode + ',')
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
@crossdomain(origin='*')
def return_item():
    secret = request.form['secret']
    if secret != SECRET_KEY:
        return abort(403)

    item_barcode = request.form['item_barcode']
    hacker_barcode = request.form['hacker_barcode']

    selected_item = None
    for item in Item.query.all():
        if item_barcode in item.item_barcodes:
            selected_item = item
    if not selected_item:
        abort(404)
    selected_item.quantity_left += 1

    hacker = Hacker.query.filter_by(barcode=hacker_barcode).first()
    if hacker:
        hacker.items_checked_out = hacker.items_checked_out.replace(item_barcode + ',', '')
    db.session.commit()

    hacker_json = {
        'id': hacker.id,
        'barcode': hacker.barcode,
        'items_checked_out': hacker.items_checked_out
    }
    return jsonify(hacker_json)

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0')
