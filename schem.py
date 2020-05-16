from marshmallow import fields, Schema


class StoreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    address = fields.String()


class CardSchema(Schema):
    id = fields.Integer(dump_only=True)
    bonus = fields.Integer()
    level = fields.Integer()


class PurchasesSchema(Schema):
    id = fields.Integer(dump_only=True)
    card_id = fields.Integer()
    store_id = fields.Integer()
    total = fields.Integer()
    bonus_earned = fields.Integer()
    bonus_spent = fields.Integer()
