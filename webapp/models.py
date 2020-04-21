from flask import Flask
from wtforms import StringField, DateField
from flask_wtf.file import FileField
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

class Event(db.Document):
    event_id = db.StringField(unique=True, required=True)
    name = db.StringField(required=True)
    event_date = db.DateField(required=True)
    location1 = db.StringField(required=True)
    location2 = db.StringField(required=True)
    location3 = db.StringField(required=True)
    scheme1 = db.FileField(required=True, collection_name='images')
    scheme2 = db.FileField(required=True, collection_name='images')
    scheme3 = db.FileField(required=True, collection_name='images')
    list_reports = db.StringField(required=True)
    calendar = db.StringField(required=True)
    about = db.StringField(required=True)

    def __unicode__(self):
        return '<event_id {} event_name {}>'.format(self.event_id, self.name)
