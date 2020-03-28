# OLD
#from flask.ext import foo => import flask_foo as foo
#from flask.ext.foo import bam => from flask_foo import bam

from flask import Flask, url_for, redirect, render_template, request, flash
from flask_mongoengine import MongoEngine

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import form, fields, validators

from werkzeug.security import generate_password_hash, check_password_hash

import flask_admin as admin
import flask_login as login
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import helpers, Admin, BaseView, expose

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# MongoDB settings
app.config['MONGODB_SETTINGS'] = {'DB': 'test'}
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


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField('Login', validators=[validators.required], render_kw={"class": "form-control"})
    password = fields.PasswordField('Password', validators=[validators.required], render_kw={"class": "form-control"})

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


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.setup_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()


# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class
class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    @expose('/bot_ed/')
    def bot_ed(self):
        return self.render('bot_ed.html')

# Flask views
@app.route('/')
def index():
    title = '_____'
    return render_template('index.html', page_title=title, user=login.current_user)


@app.route('/login/', methods=('GET', 'POST'))
def login_view():
    title = 'Авторизация'
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = form.get_user()
        login.login_user(user)
        flash('Авторизация успешна')
        return redirect(url_for('index'))

    return render_template('form.html', page_title=title, form=form)


@app.route('/register/', methods=('GET', 'POST'))
def register_view():
    title = 'Регистрация'
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User()
        form.populate_obj(user)
        user.save()
        login.login_user(user)
        flash('Регистрация успешна')
        return redirect(url_for('index'))

    return render_template('form.html', page_title=title, form=form)


@app.route('/logout/')
def logout_view():
    login.logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize flask-login
    init_login()

    # Create admin
    admin = admin.Admin(app, 'Админ-панель', index_view=MyAdminIndexView())

    # Add view
    admin.add_view(MyModelView(User))
    admin.add_view(MyAdminIndexView(name='Редактор бота'))
    admin.init_app(app)

    # Start app
    app.run(debug=True)