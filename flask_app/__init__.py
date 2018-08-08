from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from config import basedir
from flask_mail import Mail
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, WSNAME, WARN_LEVEL, MAX_SEARCH_RESULTS, subj_dict

flask_app = Flask(__name__)
flask_app.config.from_object('config')
db = SQLAlchemy(flask_app)
mail = Mail(flask_app)

from flask_app import views, models
