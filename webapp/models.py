from flask import flash, redirect, url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView

import flask_admin as admin
import flask_login as login

# Create customized model view class
class MyModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

class MyAdminView(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('bot_ed.html')

class MyAdminVote(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('vote.html')

class ExitAdmin(admin.BaseView):
    @admin.expose('/')
    def logout_view(self):
        login.logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))
