from flask import request, jsonify
from . import api
from app.schemas.user_schema import ContactMessageSchema
from datetime import datetime
from app.extensions import mongo
from marshmallow import ValidationError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_mail import Message
from flask import current_app
from app.extensions import mail

import requests
import os

RECAPTCHA_SECRET_KEY = "6Ldp00IrAAAAANpbVge59XDi83eleT7HaKbmaUYI"


@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})


@api.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        captcha_response = data.get('recaptcha')

                # Verify captcha with Google
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': captcha_response
        }
        captcha_verify = requests.post(verify_url, data=payload)
        captcha_result = captcha_verify.json()

        if not captcha_result.get('success'):
            return jsonify({'error': 'Invalid CAPTCHA'}), 400

        if not data:
            return jsonify({'status': 'error', 'message': 'Missing JSON data'}), 400
        
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

        schema = ContactMessageSchema()
        data.pop('recaptcha', None)
        validated_data = schema.load(data)

        validated_data['created_at'] = datetime.utcnow()

        name = validated_data.get('name')
        email = validated_data.get('email')
        message = validated_data.get('message')

        # Save to DB
        result = mongo.db.contact_messages.insert_one(validated_data)

        # Compose the email
        msg = Message(
            subject='Contact from portfolio',
            recipients=['amanjhavdjs12tha@gmail.com','amanjha8503@gmail.com'],
            body=f"Name: {name}\nEmail: {email}\n\nMessage: {message}\n \nIP Address: {ip_address}",
        )

        mail.send(msg)

        return jsonify({'status': 'success', 'message': 'Email sent and saved'}), 200

    except ValidationError as ve:
        return jsonify({'status': 'error', 'errors': ve.messages}), 400
    except Exception as e:
        current_app.logger.error("Error while sending email: %s", str(e))
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

@api.route("/test", methods=["GET"])
def test_mongo():
    uri = "mongodb+srv://aman:aman@mediaplayercluster.ggsfnxd.mongodb.net/?retryWrites=true&w=majority&appName=mediaPlayerCluster"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return jsonify({'status': 'success', 'message': 'retrieve messages'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': 'retrieve messages'}), 500



@api.route("/smoke", methods=["GET"])
def smoke():
    try:
        mongo.db.command("ping")
        return jsonify(status="ok", message="Mongo is connected"), 200
    except Exception as err:
        return jsonify(status="error", message=str(err)), 500
