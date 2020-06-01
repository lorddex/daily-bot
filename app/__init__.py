import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from app.middleware import SlackSignCheckMiddleware

app = Flask(__name__, static_folder=None)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.Config'
)
app.config.from_object(app_settings)
db = SQLAlchemy(app)

#app.wsgi_app = SlackSignCheckMiddleware(app.wsgi_app)

from app import views, middleware
