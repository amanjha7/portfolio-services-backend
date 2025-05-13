from flask import request,jsonify
from . import api
from app.models.message import ContactMessage
from app.schemas.user_schema import ContactMessageSchema 
from datetime import datetime
from app.extensions import db

@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

@api.route('/send-email', methods=['POST'])  # <-- Use POST not GET
def send_email():
    data = request.get_json()
    print("Received email form data:", data)

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Message: {message}")

    new_message = ContactMessage(
        name=name,
        email=email,
        message=message,
        created_at=datetime.utcnow()
    )

    db.session.add(new_message)
    db.session.commit()

    # You can also send a dummy success response
    return jsonify({'status': 'success', 'message': 'Email received'}), 200


@api.route('/messages', methods=['GET'])
def get_all_messages():
    # Fetch all messages ordered by created_at DESC (latest first)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    
    # Serialize with Marshmallow
    schema = ContactMessageSchema(many=True)
    result = schema.dump(messages)

    return jsonify(result), 200