from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import User, Store, Tag, Item

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password_hash']
        load_instance = True

class StoreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Store
        include_fk = True
        load_instance = True

class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        include_fk = True
        load_instance = True

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_fk = True
        load_instance = True