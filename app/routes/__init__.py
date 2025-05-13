from flask import Blueprint

api = Blueprint('api', __name__)

from . import sample  # Import your route files here
