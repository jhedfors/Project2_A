from system.core.controller import *

class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)
        self.load_model('Quote')
        self.db = self._app.db
    def quotes_view(self):
        data = {}
        data['non_favorites'] = self.models['Quote'].show_non_favorites(session['active_id'])
        data['favorites'] = self.models['Quote'].show_favorites(session['active_id'])
        return self.load_view('quotes_view.html', data = data)
    def add_form(self):
        info = self.models['Quote'].add_quote(request.form)
        if 'errors' in info:
            info['add_form'] = request.form
            flash(info)
        return redirect('/quotes')
    def destroy(self,quote_id):
        self.models['Quote'].destroy(quote_id)
        return redirect('/quotes')
    def add_list(self,quote_id):
        self.models['Quote'].add_list(session['active_id'],quote_id)
        return redirect('/quotes')
    def remove_list(self,quote_id):
        self.models['Quote'].remove_list(session['active_id'],quote_id)
        return redirect('/quotes')
