from flask import Flask, render_template, redirect, request, session
from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes')
def go_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    recipes=Recipe.get_all()
    return render_template("recipes.html", user=User.get_by_id(data), all_recipes = recipes)

@app.route('/view_recipe_page/<int:recipes_id>')
def view_recipe(recipes_id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template("view_recipe_page.html", recipe = Recipe.get_recipe_w_user(recipes_id))

@app.route('/user/<int:id>')
def show_user(id):
    data = {
        "id": id
    }
    return render_template('recipes.html')

@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new.html', all_users=User.get_all())

@app.route('/new_recipe', methods=['POST'])
def save():
    if not Recipe.validate_recipe(request.form):
        return redirect('/new')
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    Recipe.save(request.form)
    return redirect('/recipes')

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/new')
    if 'user_id' not in session:
        return redirect('/')
        '''
    data = {
        "name" :  request.form["name"],
        "date":  request.form["date"],
        "description":  request.form["description"],
        "instructions":  request.form["instructions"],
        "under30":  int(request.form["under30"]),
        "user_id": session["user_id"]
    }
    '''
    print("<*20")
    Recipe.save(request.form)
    return redirect('/recipes')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    print("I'm printing for testing")
    return render_template('edit.html', recipe=Recipe.get_one(data))

@app.route('/edit/recipe', methods=['POST'])
def update():
    if not Recipe.validate_recipe(request.form):
        return redirect('/edit')
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "name" :  request.form["name"],
        "updated_at":  request.form["updated_at"],
        "description":  request.form["description"],
        "instructions":  request.form["instructions"],
        "under30":  int(request.form["under30"]),
        "id": request.form['id']
    }
    print(request.form, "*" * 50)
    Recipe.update(data)
    return redirect('/recipes')

@app.route('/delete/<int:id>')
def delete(id):
    Recipe.delete(id)
    if 'user_id' not in session:
        return redirect('/')
    return redirect('/recipes')
