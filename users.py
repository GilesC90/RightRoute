from flask import render_template,redirect,session,request, flash

from project_app import app, Bcrypt
from project_app.models.route import Route

from project_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route ('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    user_data = { 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "location" : request.form['location'],
        "height" : request.form['height'],
        "weight" : request.form['weight'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['id'] = User.create(user_data)
    return redirect('/dashboard')

@app.route ('/view_profile/<id>')
def view(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id':id
    }
    this_user = User.choose_user(data)
    user = User.read_user(id = session['id'])
    total_completed = Route.total_completed({'users_id' : id })['TotalRoutes']
    print(total_completed)
    return render_template("view_profile.html", this_user = this_user, user = user, total_completed = total_completed)

@app.route('/edit_profile/<id>')
def edit_profile(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id':id
    }
    this_user = User.choose_user(data)
    user = User.read_user(id = session['id'])
    return render_template('edit_profile.html', this_user = this_user, user = user)
    
@app.route ('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.read_user(email = request.form['login_email'])
    session['id'] = user.id
    return redirect('/dashboard')

@app.route ('/logout')
def logout():
    session.clear()
    return redirect('/')
















# API Key - AIzaSyBMEfpyyg8IvUyGHA95MKRSSD_STqQilVY