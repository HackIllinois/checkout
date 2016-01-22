import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(320))
    quantity_left = db.Column(db.Integer)

    def __init__(self, name, description, quantity_left):
        self.name = name
        self.description = description
        self.quantity_left = int(quantity_left)

    def __repr__(self):
        return '<Item %r>' % self.name

class Hacker(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.Integer)
    items_checked_out = db.Column(db.String(320))

    def __init__(self, barcode, items_checked_out):
        self.barcode = barcode
        self.items_checked_out = items_checked_out

    def __repr__(self):
        return '<Hacker %r>' % self.barcode