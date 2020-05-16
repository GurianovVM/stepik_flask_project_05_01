from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    card = db.relationship('Card')


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    bonus = db.Column(db.Integer)
    level = db.Column(db.Integer)
    purchases = db.relationship('Purchas')


class Purchas(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    card = db.relationship('Card')
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('Store')
    total = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    bonus_earned = db.Column(db.Integer)
    bonus_spent = db.Column(db.Integer)


class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.Text)
