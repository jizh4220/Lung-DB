import os
import logging
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# load env
load_dotenv(os.path.join(basedir, '.flaskenv'))

# log dir
log_dir = os.path.join(basedir, os.getenv('LOG_DIR', 'logs'))

class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///books.db'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123654@localhost:5432/accession_celldata_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LOG_LEVEL = logging.INFO