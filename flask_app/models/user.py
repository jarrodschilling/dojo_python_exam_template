from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
# ------->>>>>-____ CHANGE THIS ----........>>>>>><<<<<<<
    db = "testing_login_schema"
# ------->>>>>-____ CHANGE THIS ----........>>>>>><<<<<<<
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.creates_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_one(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return results


    # GET USER BY ANYTHING, just COPY and change WHERE statement and Method NAME
    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = """SELECT * FROM users WHERE email = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def check_email(cls, data):
        data = {
            'email': data
        }
        query = """SELECT email FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) > 1:
            return True
        
    

    # DOUBLE CHECK THIS, may or may NOT need all of it.
    # ALSO may need to change parameters
    @staticmethod
    def validate_reg(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 character", 'reg')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 character", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email format", 'reg')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match", 'reg')
            is_valid = False

        # IS THIS ONE NEEDED???
        if re.search('[0-9]', data['password']) is None:
            flash("Password must contain a number", 'reg')
            is_valid = False

        # IS THIS ONE NEEDED???
        if re.search('[A-Z]', data['password']) is None:
            flash("Password must contain a capital letter", 'reg')
            is_valid = False

        if User.check_email(data['email']) == True:
            flash("Email already exists", 'reg')
            is_valid = False

        return is_valid