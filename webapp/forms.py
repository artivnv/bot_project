from wtforms import BooleanField, PasswordField, form, validators, DateField, TextField

import flask_login as login

from models import *

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = TextField('Login', validators=[validators.required], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[validators.required], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember', default=True, render_kw={"class": "form-check-input" "form-check-label"})

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.objects(login=self.login.data).first()

class RegistrationForm(form.Form):
    login = TextField(validators=[validators.required])
    email = TextField()
    password = PasswordField(validators=[validators.required])

    def validate_login(self, field):
        if User.objects(login=self.login.data):
            raise validators.ValidationError('Duplicate username')

class EventForm(form.Form):
    name = TextField(validators=[validators.required])
    event_date = DateField(validators=[validators.required])
    list_reports = TextField(validators=[validators.required])
