from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
# ------->>>>>-____ CHANGE THIS ----........>>>>>><<<<<<<
    db = "prep_exam_schema"
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

    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
        
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        user = User.get_user_by_email(data)
        if user:
            flash("Please use another email")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First name must be atleast 2 characters long")
            is_valid = False
        
        return is_valid