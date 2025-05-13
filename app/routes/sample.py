from flask import jsonify
from . import api

@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})
