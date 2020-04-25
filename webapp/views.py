from flask import flash, redirect, url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView
from flask.views import MethodView
from wtforms import form

import flask_admin as admin
import flask_login as login

from forms import EventForm

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

    @admin.expose_plugview('/upload/')
    class Upload(MethodView):

        def post(self, cls):
            title = 'Отправка данных в базу'
            form = EventForm(request.form)
            print(request.form)

            #form.file.data.save()
            flash('Данные о мероприятии записались в базу')
            return cls.render('index.html', request=request, name="upload")


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
