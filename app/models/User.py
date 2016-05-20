from system.core.model import Model
from flask.ext.bcrypt import Bcrypt
import re
from datetime import datetime
import time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(.{8,})$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    def login(self,post):
        errors = {}
        if len(post['email'])< 1:
            errors['login_email'] = u'Email cannot be empty!'
        if len(post['password'])< 1:
            errors['login_password'] = u'Password cannot be empty!'
        if len(errors) > 0:
            return {'errors': errors}
        query = "SELECT id, name, alias, password FROM users WHERE email = :email"
        values = {'email': post['email']}
        db = self.db.query_db(query,values)
        if(db):
            db = db[0]
            match = self.bcrypt.check_password_hash(db['password'],post['password'])
            if(match):
                return db
        errors['login_password'] = u'Invalid Email or Password!'
        return {'errors': errors}

    def register(self,post):
        errors = {}
        if len(post['name'])< 3:
            errors['name'] = u'Name cannot be empty!'
        if len(post['alias'])< 3:
            errors['alias'] = u'Alias cannot be empty!'
        if len(post['email'])< 3:
            errors['email'] = u'Email cannot be empty!'
        elif not EMAIL_REGEX.match(post['email']):
            errors['email'] = u"Invalid Email Address!"
        if not PASSWORD_REGEX.match(post['password']):
            errors['password'] = u"Password must be at least 8 characters,and contain at least 1 uppercase letter and one number!"
        if not post['confirm_password'] == post['password']:
            errors['confirm_password'] = u"Password and Confirmation must match!"
        if len(post['dob'])< 1:
            errors['dob'] = u'Date of Birth cannot be empty!'
        elif datetime.strptime(post['dob'], "%Y-%m-%d") > datetime.now():
            errors['dob'] = u'Date of Birth must be in the past!!'
        if(self.show(post['email'])):
            errors['email'] = u"Email already exists!"
        if len(errors) > 0:
            return {'errors': errors}
        pw_hash = self.bcrypt.generate_password_hash(post['password'])
        query = "INSERT INTO users (name, alias, email, password, dob, created_at, modified_at) VALUES (:name, :alias, :email, :password, :dob, NOW(), NOW())"
        values = {'name' : post['name'], 'alias': post['alias'], 'email': post['email'],'password': pw_hash, 'dob': post['dob']}
        active_id = self.db.query_db(query,values)
        return {'active_id': active_id}
    def show(self, email):
        query = "SELECT email FROM users WHERE email = :email"
        values = {'email':email}
        return self.db.query_db(query,values)
