from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Example:
# ------->>>>>-____ CHANGE THIS ----........>>>>>><<<<<<<
    db = "prep_exam_schema"
# ------->>>>>-____ CHANGE THIS ----........>>>>>><<<<<<<
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.content = data['content']
        self.title = data['title']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def save_example(cls, data):
        query = """INSERT INTO examples (name, description, content, title, user_id)
                VALUES (%(name)s, %(description)s, %(content)s, %(title)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one_example(cls, data):
        query = """SELECT * FROM examples WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def get_all_examples(cls):
        query = """SELECT * FROM examples
                LEFT JOIN users ON users.id = examples.user_id"""
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return False
        pass