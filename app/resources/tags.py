from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Tag, Store
from ..schemas import TagSchema

tags_bp = Blueprint('tags', __name__, url_prefix='/tag')

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

@tags_bp.route('/store/<int:store_id>', methods=['POST'])
@jwt_required()
def create_tag(store_id):
    store = Store.query.get_or_404(store_id)
    if store.user_id != int(get_jwt_identity()):  # CHANGED: Added int()
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    tag = Tag(name=data['name'], store_id=store_id)
    db.session.add(tag)
    db.session.commit()
    return tag_schema.dump(tag), 201

@tags_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_tag(id):
    tag = Tag.query.get_or_404(id)
    if tag.store.user_id != int(get_jwt_identity()):  # CHANGED: Added int()
        return jsonify({'message': 'Unauthorized'}), 401
    return tag_schema.dump(tag)

@tags_bp.route('/store/<int:store_id>/s', methods=['GET'])  # /store/<id>/tags
@jwt_required()
def get_tags_in_store(store_id):
    store = Store.query.get_or_404(store_id)
    if store.user_id != int(get_jwt_identity()):  # CHANGED: Added int()
        return jsonify({'message': 'Unauthorized'}), 401
    tags = Tag.query.filter_by(store_id=store_id).all()
    return tags_schema.dump(tags)

@tags_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    if tag.store.user_id != int(get_jwt_identity()):
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Deleted'})