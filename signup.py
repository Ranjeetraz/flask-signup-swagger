from flask import request
from flask_restx import Resource, Namespace, fields
from mysql_connection import mycursor, mydb_connection

# Create a namespace for the POST method
signup_namespace = Namespace('post_method', description='POST method namespace')

# Define the request body model for the POST method
request_body_model = signup_namespace.model('RequestBody', {
    'email': fields.String(description='Email address', format='email'),
    'password': fields.String(description='Password', format='password'),
    'username': fields.String(description='Username'),
    'AccessToken': fields.String(description='Access Token'),
    'RefreshToken': fields.String(description='Refresh Token'),
    
})

class Signup(Resource):
    @signup_namespace.doc()
    @signup_namespace.expect(request_body_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        filter_query = "select * from signup_table where email = '{}'".format(email)
        mycursor.execute(filter_query)
        existing_user = mycursor.fetchone()
        if existing_user:
            return {'message': f'This Email:- {email} already exists'}, 400
        else:
            insert_query = "insert into signup_table (username, email, password) VALUES (%s, %s, %s)"
            insert_value = (username, email, password)
            mycursor.execute(insert_query, insert_value)
            mydb_connection.commit()
            print(mycursor.rowcount, "record inserted.")
            return {'message': ' Account created successfully', 'email': email}, 201


