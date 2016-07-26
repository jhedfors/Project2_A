
from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/register'] = 'Users#register'
routes['POST']['/login'] = 'Users#login'
routes['GET']['/quotes'] = 'Quotes#quotes_view'
routes['GET']['/destroy/<int:quote_id>'] = 'Quotes#destroy'
routes['GET']['/add_list/<int:quote_id>'] = 'Quotes#add_list'
routes['GET']['/remove_list/<int:quote_id>'] = 'Quotes#remove_list'
routes['GET']['/users/<id>'] = 'Users#user_view'
routes['POST']['/add_form'] = 'Quotes#add_form'
routes['GET']['/logout'] = 'Users#logout'
