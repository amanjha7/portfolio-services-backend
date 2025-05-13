from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models.message import ContactMessage

class ContactMessageSchema(SQLAlchemySchema):
    class Meta:
        model = ContactMessage
        load_instance = True

    id = auto_field()
    name = auto_field()
    email = auto_field()
    message = auto_field()
    created_at = auto_field()
