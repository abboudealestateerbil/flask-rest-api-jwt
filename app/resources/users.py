from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from .. import db, jwt_token_blacklist
from ..models import User
from ..schemas import UserSchema
from werkzeug.security import check_password_hash

users_bp = Blueprint('users', __name__, url_prefix='/user')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User exists'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))  # Changed: Convert to string
        refresh_token = create_refresh_token(identity=str(user.id))  # Changed: Convert to string
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    return jsonify({'message': 'Invalid credentials'}), 401

@users_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_token_blacklist.add(jti)  # Revoke access
    # For refresh, you'd need to pass it separately or handle in client; for simplicity, assume client discards
    response = jsonify({'message': 'Logged out'})
    unset_jwt_cookies(response)  # Clears cookies if used, but since bearer, optional
    return response

@users_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)

@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    if int(get_jwt_identity()) != user.id:  # Changed: Convert identity back to int
        return jsonify({'message': 'Unauthorized'}), 401
    return user_schema.dump(user)

@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    if int(get_jwt_identity()) != user.id:  # Changed: Convert identity back to int
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Deleted'})