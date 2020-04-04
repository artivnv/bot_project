from flask import Flask
from wtforms import StringField
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mongoengine import MongoEngine

import flask_login as login

# Create application
app = Flask(__name__)
app.config.from_pyfile('config.py')

# MongoDB settings
db = MongoEngine()
db.init_app(app)

# Create user model. For simplicity, it will store passwords in plain text.
class User(db.Document):
    login = db.StringField(max_length=80, unique=True)
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=64)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Required for administrative interface
    def __unicode__(self):
        return '<User name={} id={}>'.format(self.login, self.id)
