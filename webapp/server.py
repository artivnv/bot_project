from flask import flash, redirect, request, render_template, url_for

from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from wtforms import form

import flask_admin as admin
import flask_login as login

from views import *
from forms import *

# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.setup_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()

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
        login.login_user(user, remember=form.remember_me.data)
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
    admin.add_view(MyAdminView(name="Редактор бота"))
    admin.add_view(MyAdminVote(name="Результаты голосования"))
    admin.add_view(ExitAdmin(name="Выход"))

    # Start app
    app.run(debug=True)