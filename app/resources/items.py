from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Item, Store
from ..schemas import ItemSchema

items_bp = Blueprint('items', __name__, url_prefix='/item')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    store = Store.query.get_or_404(data['store_id'])
    if store.user_id != int(get_jwt_identity()):  # ADDED int() HERE
        return jsonify({'message': 'Unauthorized'}), 401
    item = Item(name=data['name'], price=data['price'], store_id=data['store_id'])
    db.session.add(item)
    db.session.commit()
    return item_schema.dump(item), 201

@items_bp.route('/s', methods=['GET'])  # /items
@jwt_required()
def get_all_items():
    # For simplicity, get all items owned by user's stores
    stores = Store.query.filter_by(user_id=int(get_jwt_identity())).all()  # ADDED int() HERE
    store_ids = [s.id for s in stores]
    items = Item.query.filter(Item.store_id.in_(store_ids)).all()
    return items_schema.dump(items)

@items_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_item(id):
    item = Item.query.get_or_404(id)
    if item.store.user_id != int(get_jwt_identity()):  # ADDED int() HERE
        return jsonify({'message': 'Unauthorized'}), 401
    return item_schema.dump(item)

@items_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_item(id):
    item = Item.query.get_or_404(id)
    if item.store.user_id != int(get_jwt_identity()):  # ADDED int() HERE
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    if 'store_id' in data:
        new_store = Store.query.get_or_404(data['store_id'])
        if new_store.user_id != int(get_jwt_identity()):  # ADDED int() HERE
            return jsonify({'message': 'Unauthorized'}), 401
        item.store_id = data['store_id']
    db.session.commit()
    return item_schema.dump(item)

@items_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    item = Item.query.get_or_404(id)
    if item.store.user_id != int(get_jwt_identity()):  # ADDED int() HERE
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'})