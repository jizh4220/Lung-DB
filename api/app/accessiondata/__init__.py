from flask import Blueprint
accessiondata_bp = Blueprint('accessiondata_bp',__name__)
from app.accessiondata import routes