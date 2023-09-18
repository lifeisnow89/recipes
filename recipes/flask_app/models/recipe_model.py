from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class Recipe:
    db = 'recipes'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions'] 
        self.under30 = data['under30']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = None

    @classmethod
    def get_recipe_w_user(cls, id):
        data = {'id' : id}
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.users_id = users.users_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        recipe = cls(results[0])
        print(results[0])
        recipe.posted_by = results[0]['first_name'] 
        print('*************************', 
            recipe.posted_by, 
        '***********************************')
        return recipe 

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes where id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return cls( results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.users_id = users.users_id;"
        results = connectToMySQL('recipes').query_db(query)
        print(results)
        recipes = []
        for recipe in results:
            new_recipe = cls(recipe)
            new_recipe.posted_by = recipe['first_name']
            recipes.append(new_recipe)
        return recipes

    @classmethod
    def save(cls, form_data):
        query = "INSERT INTO recipes (name, description, instructions, under30, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(users_id)s)"
        results = connectToMySQL('recipes').query_db(query, form_data)
        return results

    @classmethod
    def update(cls, form_data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, updated_at=NOW() WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, form_data)
        return results

    @classmethod
    def delete(cls, id):
        #data = {'id' : id}
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        
        results = connectToMySQL('recipes').query_db(query, {"id": id})
        return results

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            flash("Name must be at least 2 characters, all fields required.")
            is_valid = False
        if len(recipe['description']) < 2:
            flash("Description must be at least 2 characters, all fields required.")
        if len(recipe['instructions']) <2:
            is_valid = False
            flash("Instructions must be at least 2 characters, all fields required.")
        if recipe['updated_at'] == "":
            is_valid = False
            flash("Please enter date, all fields required")
        return is_valid