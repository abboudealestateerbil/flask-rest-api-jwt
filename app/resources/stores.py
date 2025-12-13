from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Store
from ..schemas import StoreSchema

stores_bp = Blueprint('stores', __name__, url_prefix='/store')

store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)

@stores_bp.route('/', methods=['POST'])
@jwt_required()
def create_store():
    data = request.get_json()
    store = Store(name=data['name'], user_id=int(get_jwt_identity()))  # CHANGED: Added int()
    db.session.add(store)
    db.session.commit()
    return store_schema.dump(store), 201

@stores_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_store(id):
    store = Store.query.get_or_404(id)
    if store.user_id != int(get_jwt_identity()):  # CHANGED: Added int()
        return jsonify({'message': 'Unauthorized'}), 401
    return store_schema.dump(store)

@stores_bp.route('/s', methods=['GET'])  # /stores for all
@jwt_required()
def get_all_stores():
    stores = Store.query.filter_by(user_id=int(get_jwt_identity())).all()  # CHANGED: Added int()
    return stores_schema.dump(stores)

@stores_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_store(id):
    store = Store.query.get_or_404(id)
    if store.user_id != int(get_jwt_identity()):  # CHANGED: Added int()
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(store)
    db.session.commit()
    return jsonify({'message': 'Deleted'})