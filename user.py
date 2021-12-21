from project_app.config.mysqlconnection import MySQLConnection, connectToMySQL

from flask import flash

from project_app import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

import os
print( os.environ.get("FLASK_APP_API_KEY") )

class User:
    db = 'project'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.location = data['location']
        self.height = data['height']
        self.weight = data['weight']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create(cls, data):
        query = ''' INSERT INTO users 
                    (first_name, last_name, email, location, height, weight, password) 
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(location)s, %(height)s, %(weight)s, %(password)s);
                '''
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def choose_user (cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        this_route = cls(result[0])
        return this_route

    @classmethod
    def read_user(cls,**data):
        query = 'SELECT * FROM users WHERE ' + ' AND '.join(f'`{col}`=%({col})s' for col in data) + ';'

        results = connectToMySQL(cls.db).query_db(query, data)

        if results:
            return cls(results[0])

    @classmethod
    def update_profile(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, location = %(location)s, height = %(height)s, weight = %(crust)s, password = %(password)s updated_at = NOW() WHERE id = %(id)s;" 
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod
    def validate_register(data):
        errors = {}
        if len(data['first_name']) < 2:
            errors['first_name'] = "First name needs to be longer."
            
        if len(data['last_name']) < 2:
            errors['last_name'] = "Last name needs to be longer."
            
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email."
            
        elif User.read_user(email = data['email']):
            errors['email'] = "Email already in use"

        if len(data['location']) < 2:
            errors['location'] = "Location needs to be longer."

        if len(data['height']) < 1:
            errors['height'] = "Height should be taller."

        if len(data['weight']) < 2:
            errors['weight'] = "Weight should be heavier."

        if len(data['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long."
            
        if data['password_confirmation'] != data['password']:
            errors['password_confirmation'] = "Passwords do not match"
            

        for category, message in errors.items():
            flash(message, category)
        
        return len(errors) == 0

    @staticmethod
    def validate_login(data):
        errors = {}
        user = User.read_user(email = data['login_email'])
        if not user:
            errors['login'] = "Invalid Login Credentials."
            
        elif not bcrypt.check_password_hash(user.password,data['login_password']):
            errors['login'] = "Invalid Login Credentials."

        for category, message in errors.items():
            flash(message, category)
        
        return len(errors) == 0