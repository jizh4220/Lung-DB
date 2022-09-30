import os
import logging
from logging.handlers import RotatingFileHandler
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config, log_dir
from app.utils.log import DayRotatingHandler
from app.utils import responses as resp
from app.utils.responses import response_with
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()
cors = CORS()
jwt = JWTManager()
migrate = Migrate()
marshmallow = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__,
                static_folder='../../dist',
                template_folder="../../dist",
                static_url_path='/')
    app.config.from_object(config_class)

     # plugin
    register_plugins(app)

    # blueprint
    register_blueprints(app)

    # logging
    register_logging(app)

    # error
    register_errors(app)

    app.logger.info('Flask Rest Api startup On MAC')
    #cors = CORS(app, supports_credentials=True)
    return app

def register_logging(app):
    app.logger.name = 'flask_api'
    log_level = app.config.get("LOG_LEVEL", logging.INFO)
    cls_handler = logging.StreamHandler()
    log_file = os.path.join(log_dir, datetime.date.today().strftime("%Y-%m-%d.log"))
    file_handler = DayRotatingHandler(log_file, mode="a", encoding="utf-8")

    logging.basicConfig(level=log_level,
                        format="%(asctime)s %(name)s "
                               "%(filename)s[%(lineno)d] %(funcName)s() %(levelname)s: %(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        handlers=[cls_handler, file_handler])

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(os.path.join(log_dir, 'flask_api.log'),maxBytes=1024 * 1024 * 50, backupCount=5, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(name)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))

            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)


def register_plugins(app):
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    marshmallow.init_app(app)
    migrate.init_app(app, db)
    

def register_blueprints(app):
    #blueprint registration
    from app.author import author_bp
    app.register_blueprint(author_bp,url_prefix='/author')

    from app.book import book_bp
    app.register_blueprint(book_bp,url_prefix='/book')
    
    from app.user import user_bp
    app.register_blueprint(user_bp,url_prefix='/user')
    
    from app.wordcloud import wordcloud_bp
    app.register_blueprint(wordcloud_bp,url_prefix='/wordcloud')

    from app.accessiondata import accessiondata_bp
    app.register_blueprint(accessiondata_bp,url_prefix='/accessiondata')

    swaggerui_blueprint = get_swaggerui_blueprint('/api/docs','/api/spec',config={'app_name':'Flask API Docs'})
    app.register_blueprint(swaggerui_blueprint,url_prefix='/api/docs')


def register_errors(app):

    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)