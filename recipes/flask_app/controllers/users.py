from flask import Flask, flash, render_template,redirect,request,session
from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_reg.html')


@app.route('/register', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,

    }
    id = User.save(data)
    session['user_id'] = id
    return redirect("/recipes")

@app.route('/login',methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')