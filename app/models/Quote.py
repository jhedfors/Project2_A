from system.core.model import Model

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()
    def add_quote(self, post):
        errors ={}
        if len(post['speaker'])< 4:
            errors['speaker'] = u'Speaker name must be more than 3 characters!'
        if len(post['quote'])< 11:
            errors['quote'] = u'Quote must be more than 10 characters!'
        if len(errors) > 0:
            return {'errors': errors}
        query = "INSERT INTO quotes (user_id, speaker, quote, created_at, modified_at) VALUES(:user_id, :speaker, :quote, NOW(),NOW())"
        values = {'user_id' : post['active_id'], 'speaker' : post['speaker'], 'quote':post['quote']}
        return {self.db.query_db(query, values)}
    def show_favorites(self, active_id):
        query = "SELECT quotes.id as quote_id, users.id as poster_id, users.alias as alias, speaker, quote from quotes LEFT JOIN users ON users.id = quotes.user_id LEFT JOIN favorites on favorites.quote_id = quotes.id WHERE favorites.user_id = :active_id"
        values = {'active_id':active_id}
        return self.db.query_db(query,values)
    def show_non_favorites(self, active_id):
        query = "SELECT DISTINCT quotes.id as quote_id, users.id as poster_id, users.alias as alias, speaker, quote from quotes LEFT JOIN users ON users.id = quotes.user_id LEFT JOIN favorites on favorites.quote_id = quotes.id WHERE NOT quotes.id in (SELECT quotes.id from quotes LEFT JOIN users ON users.id = quotes.user_id LEFT JOIN favorites on favorites.quote_id = quotes.id WHERE favorites.user_id = :active_id )"
        values = {'active_id':active_id}
        return self.db.query_db(query,values)
    def add_list(self, active_id, quote_id):
        query = "INSERT INTO favorites (user_id, quote_id) VALUES (:user_id, :quote_id)"
        values = {'user_id':active_id,'quote_id':quote_id}
        return self.db.query_db(query,values)
    def remove_list(self, active_id, quote_id):
        query = "DELETE FROM favorites WHERE user_id = :user_id AND quote_id =:quote_id"
        values = {'user_id':active_id,'quote_id':quote_id}
        return self.db.query_db(query,values)
    def show_all_quotes_user(self, user_id):
        query = "SELECT users.alias as alias, speaker, quote from quotes LEFT JOIN users ON users.id = quotes.user_id WHERE users.id = :user_id"
        values = {'user_id':user_id}
        return self.db.query_db(query,values)
