from flask import request, jsonify
from . import api
from app.models.message import ContactMessage
from app.schemas.user_schema import ContactMessageSchema
from datetime import datetime
from app.extensions import db
from marshmallow import ValidationError


@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})


@api.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Missing JSON data'}), 400

        # Validate using Marshmallow schema
        schema = ContactMessageSchema()
        validated_data = schema.load(data)

        # Create new message
        new_message = ContactMessage(
            name=validated_data['name'],
            email=validated_data['email'],
            message=validated_data['message'],
            created_at=datetime.utcnow()
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Email received'}), 200

    except ValidationError as ve:
        return jsonify({'status': 'error', 'errors': ve.messages}), 400
    except Exception as e:
        db.session.rollback()
        print("Error while saving message:", str(e))
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


@api.route('/messages', methods=['GET'])
def get_all_messages():
    try:
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        schema = ContactMessageSchema(many=True)
        result = schema.dump(messages)
        return jsonify(result), 200
    except Exception as e:
        print("Error fetching messages:", str(e))
        return jsonify({'status': 'error', 'message': 'Could not retrieve messages'}), 500
