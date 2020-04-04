from wtforms import BooleanField, PasswordField, fields, form, validators

import flask_login as login

from models import *

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField('Login', validators=[validators.required], render_kw={"class": "form-control"})
    password = fields.PasswordField('Password', validators=[validators.required], render_kw={"class": "form-control"})
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
    login = fields.TextField(validators=[validators.required])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required])

    def validate_login(self, field):
        if User.objects(login=self.login.data):
            raise validators.ValidationError('Duplicate username')

