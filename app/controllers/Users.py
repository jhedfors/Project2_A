from system.core.controller import *
from datetime import datetime
import time

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Quote')
        self.db = self._app.db
    def index(self):
        return self.load_view('login_reg.html')
    def login(self):
        info = self.models['User'].login(request.form)
        info['login_form'] = request.form
        if 'errors' in info:
            flash(info)
            return redirect('/')
        print 'INFO',info

        session['active_id'] = info['id']
        session['alias'] = info['alias']
        return redirect('/quotes')
    def register(self):
        info = self.models['User'].register(request.form)
        info['reg_form'] = request.form
        print info
        if 'errors' in info:
            flash(info)
            return redirect('/')
        session['active_id'] = info['active_id']
        session['alias'] = request.form['alias']
        return redirect('/quotes')
    def user_view(self, id):

        data = self.models['Quote'].show_all_quotes_user(id)
        # print 'DATA', data
        # count =  len(data)
        return self.load_view('user_view.html', data = data, count = len(data))

    def logout(self):
        session.clear()
        return redirect('/')
