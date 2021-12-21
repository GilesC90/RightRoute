from project_app.config.mysqlconnection import MySQLConnection, connectToMySQL

from flask import flash

from project_app.models.user import User

class Route:
    db = 'project'
    def __init__(self, data):
        self.id = data['id']
        self.name = data["name"]
        self.distance = data['distance']
        self.completed = data['completed']
        self.path = data['path']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def all_routes(cls):
        query = "SELECT * FROM routes LEFT JOIN users on users.id = routes.users_id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_routes = []
        if results:
            for row in results:
                this_route = cls(row)
                data = {
                    'id' : row['users.id'],
                    'name' : row['name'],
                    'distance' : row['distance'],
                    'completed' : row['completed'],
                    'path' : row['path'],
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'location' : row['location'],
                    'height' : row['height'],
                    'weight' : ['weight'],
                    'password' : row['password'],
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }
                this_route.user = User(data)
                all_routes.append(this_route)
        return all_routes  

    @classmethod
    def total_completed(cls, data):
        query = "SELECT SUM(completed) AS TotalRoutes FROM routes WHERE users_id = %(users_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return result[0]
    @classmethod
    def create_route(cls, data):
        query = "INSERT INTO routes (name, distance, path, users_id) VALUES (%(name)s, %(distance)s, %(path)s, %(users_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def choose_route(cls,data):
        query = "SELECT * FROM routes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        this_route = cls(result[0])
        return this_route

    @classmethod
    def completed_route(cls, data):
        query = "UPDATE routes SET completed = 1, updated_at = NOW() WHERE id = %(id)s;" 
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
        
    @classmethod
    def destroy_route(cls,data):
        query  = "DELETE FROM routes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod
    def validate_route(data):
        
        errors = {}
        if len(data['name']) < 2:
            errors['name'] = "Name field needs to be longer."
            
        if len(data['distance']) < 0:
            errors['distance'] = "Run needs to be longer."

        for category, message in errors.items():
            flash(message, category)
        
        return len(errors) == 0