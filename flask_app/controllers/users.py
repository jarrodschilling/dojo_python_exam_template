from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Make sure the ROUTE is correct, sometimes the login isn't at index ('/')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_reg(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = User.save_one(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']

    return redirect('/showall')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }

    user_in_db  = User.get_user_by_email(data)

    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect('/showall')


@app.route('/showall')
def show_all():
    return render_template('show-all.html')