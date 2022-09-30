from flask import Blueprint
wordcloud_bp = Blueprint('wordcloud_bp',__name__)
from app.wordcloud import routes