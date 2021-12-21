from flask import render_template,redirect,session,request, flash, jsonify

from project_app import app, Bcrypt

from project_app.models.user import User

from project_app.models.route import Route

@app.route ('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')
    user = User.read_user(id = session['id'])
    all_routes = Route.all_routes()
    return render_template('dashboard.html', user = user, all_routes = all_routes)

@app.route('/route/create', methods=['POST'])
def create_route():
    if 'id' not in session:
        return redirect('/logout')
    if not Route.validate_route(request.json):
        return redirect('/dashboard')
    data = {
        'name': request.json['name'],
        'distance': request.json['distance'],
        'path': request.json['path'],
        'users_id': session['id']
    }
    Route.create_route(data)
    return jsonify(data)

@app.route('/route/<id>')
def get_route(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id':id
    }
    this_route = Route.choose_route(data)
    user = User.read_user(id = session['id'])
    return render_template("view_run.html", this_route = this_route, user = user)

@app.route('/route/completed', methods = ['POST'])
def complete_route():
    if 'id' not in session:
        return redirect('/logout')
    data = {
        "completed" : request.form["completed"],
        "id" : request.form["id"]
    }
    Route.completed_route(data)
    return redirect('/dashboard')
