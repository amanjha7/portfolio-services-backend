from flask import request, jsonify
from . import api
from app.schemas.user_schema import ContactMessageSchema
from datetime import datetime
from app.extensions import mongo
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

        # Use schema to validate and deserialize data
        schema = ContactMessageSchema()
        validated_data = schema.load(data)  # This should now be a dictionary, not a model

        # Add a created_at field if it's not present
        validated_data['created_at'] = datetime.utcnow()

        # Insert the validated data into MongoDB
        result = mongo.db.contact_messages.insert_one(validated_data)

        if result.inserted_id:
            return jsonify({'status': 'success', 'message': 'Email received'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Insertion failed'}), 500

    except ValidationError as ve:
        return jsonify({'status': 'error', 'errors': ve.messages}), 400
    except Exception as e:
        print("Error while saving message:", str(e))
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500



@api.route('/messages', methods=['GET'])
def get_all_messages():
    try:
        messages_cursor = mongo.db.contact_messages.find().sort("created_at", -1)
        messages = list(messages_cursor)

        # Convert ObjectId to string and dump using schema
        for msg in messages:
            msg['_id'] = str(msg['_id'])

        schema = ContactMessageSchema(many=True)
        result = schema.dump(messages)
        return jsonify(result), 200

    except Exception as e:
        print("Error fetching messages:", str(e))
        return jsonify({'status': 'error', 'message': 'Could not retrieve messages'}), 500
