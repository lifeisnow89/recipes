from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class User:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['users_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("recipes").query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes').query_db(query)
        users = []
        for d in results:
            users.append( cls(d) )
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        if len(results) < 1:
            return False
        print (results[0])
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE users_id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        if len(results) < 1:
            return False
        print (results[0])
        return cls(results[0])

    @classmethod
    def get_one_with_recipe(cls, user_id):
        query = "SELECT * FROM user LEFT JOIN recipes on users.id = recipes.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        print(results[0])
        user = cls(results[0])
        for row in results:
            n = {
                'id': row['recipes.id'],
                'recipes': row['recipes']
            }
            user.recipes.append( recipes_model.Recipe(n) )
        return user

    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM users WHERE id = %(id)s"
        results = connectToMySQL('recipes').query_db(query, {'id':users_id})
        return results

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if len(user['email']) >= 1:
            flash("Email already taken", "register")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be 8 characters or greater.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid
