from flask import Blueprint
user_bp = Blueprint('user_bp',__name__)
from app.user import routes