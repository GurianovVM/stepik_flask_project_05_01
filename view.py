import datetime
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app import app, db, jwt
from model import User, Card, Purchas, Store
from schem import StoreSchema, CardSchema, PurchasesSchema


@app.route('/')
def main_view():
    return '<h1>WORK</h1> '


@app.route('/token/<id_card>/', methods=['GET'])
def login(id_card):
    token = create_access_token(identity=id_card)
    return jsonify(access_token=token)


@app.route('/stores/', methods=['GET'])
@jwt_required
def get_stores():
    stores = db.session.query(Store).all()
    if stores:
        store_schema = StoreSchema(many=True)
        return jsonify(store_schema.dump(stores))
    else:
        return jsonify(), 404


@app.route('/cards/<id_card>/', methods=['GET'])
@jwt_required
def get_card(id_card):
    token_id = get_jwt_identity()
    if token_id == id_card:
        card = db.session.query(Card).get(id_card)
        if card:
            card_schema = CardSchema()
            return jsonify(card_schema.dump(card))
        else:
            return jsonify(), 404
    else:
        return jsonify(msg='wrong card')


@app.route('/purchases/', methods=['GET'])
@jwt_required
def get_purchases():
    token_id = get_jwt_identity()
    card = db.session.query(Card).get(token_id)
    if card:
        purchases_schema = PurchasesSchema(many=True)
        return jsonify(purchases_schema.dump(card.purchases))
    else:
        return jsonify(msg='Card is not registered'), 404


@app.route('/purchases/<id_pur>/', methods=['GET'])
@jwt_required
def get_purchase(id_pur):
    purchase = db.session.query(Purchas).get(id_pur)
    card_id = get_jwt_identity()
    if purchase and int(card_id) == purchase.card_id:
        purchase_shem = PurchasesSchema()
        return jsonify(purchase_shem.dump(purchase))
    else:
        return jsonify(msg='Wrong id'), 404


@app.route('/tokenstore/<id_store>/', methods=['GET'])
def login_store(id_store):
    store = db.session.query(Store).get(id_store)
    if store:
        token = create_access_token(identity=store.id, fresh=True)
        return jsonify(access_token=token)
    else:
        return jsonify(msg='Not store'), 404


@app.route('/cards/', methods=['POST'])
@jwt_required
def set_card():
    json_data = request.get_json()
    if json_data:
        name = json_data.get('full_name')
        if name:
            client = User(name=name)
            db.session.add(client)
            db.session.commit()
            card = Card(user_id=client.id, bonus=0, level=0)
            db.session.add(card)
            db.session.commit()
            return jsonify(id=card.id), 201
        else:
            return jsonify(msg='Not full_name'), 400
    else:
        return jsonify(msg='Bad json'), 400

@app.route('/purchase/', methods=['POST'])
@jwt_required
def set_purchase():
    json_data = request.get_json()
    if json_data:
        card = json_data.get('card')
        store = int(json_data.get('store'))
        sum = int(json_data.get('sum'))
        bonus_spent = int(json_data.get('bonus_spent'))
        if card and store and sum:
            card = db.session.query(Card).get(card)
            if (card.bonus - bonus_spent) > 0:
                bonus_earned = int(sum / 10)
                purchase = Purchas(card=card, store_id=store, total=sum, bonus_spent=bonus_spent,
                                   bonus_earned=bonus_earned, date=datetime.datetime.now())
                db.session.add(purchase)
                card.bonus = (card.bonus - bonus_spent) + bonus_earned
                db.session.commit()
                return jsonify(id=purchase.id, bonus_earned=bonus_earned), 201, {"Location":"/purchases/{}/".format(
                    purchase.id
                )}
            else:
                return jsonify(msg='Not enough bonuses'), 400
        else:
            return jsonify(msg='Bad data'), 400
    else:
        return jsonify(msg='bad json'), 400

