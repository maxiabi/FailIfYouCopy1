from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from celery import Celery

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app
app.config.from_pyfile('config.py')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models here
from .models import User, Role

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Initialize CORS
CORS(app)

# Import and register blueprints
from .api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

# Import and register admin views
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')
