from flask import request  # Import request from Flask
from flask_restx import Resource, Namespace
from signup import signup_namespace , request_body_model
from mysql_connection import mycursor, mydb_connection
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,create_refresh_token, get_jwt
from flask import Flask
from flask_restx import Api
import jwt as Jwt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secretkey'  # Change this to a secure secret key in production
api = Api(app, title='Flask RESTplus Demo', version='1.0', description='Application Flask RESTplus Signup & Login', doc='/doc')
jwt = JWTManager(app)
get_ns = Namespace('get_method', description='GET method namespace')


class Login(Resource):
    @signup_namespace.doc()
    @signup_namespace.expect(request_body_model, validate=True)
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        filter_query = "SELECT * FROM signup_table WHERE email = %s AND password = %s"
        mycursor.execute(filter_query, (email, password))
        user = mycursor.fetchone()
        if user:
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            # Convert the tokens from bytes to string
            access_token_str = access_token.decode('utf-8')
            refresh_token_str = refresh_token.decode('utf-8')

            print(access_token_str, "encoded_Token......")
            return {'message': 'Login successfully', 'email': email, 'Access Token': access_token_str, 'Refresh Token': refresh_token_str}, 200
        else:
            return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @signup_namespace.doc()
    @signup_namespace.expect(request_body_model, validate=True)
    @jwt_required(refresh=True)
    def post(self):
        data = request.json
        refresh_token = data.get('RefreshToken')  # Retrieve refresh token from request body
        # print(refresh_token,"refresh_token ............................................")
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        new_token = new_token.decode('utf-8')
        return {"access_token": new_token}, 200

    
    
class GetRecord(Resource):
    @signup_namespace.doc()
    @signup_namespace.expect(request_body_model, validate=True)
    def post(self):
        data = request.json
        access_token = data.get('AccessToken')
        decoded_jwt = Jwt.decode(access_token, 'secretkey', algorithms=['HS256'])  
        email = decoded_jwt['sub']  
        # Assuming the access token contains the user's email address
        filter_query = "SELECT * FROM signup_table WHERE email = %s "
        mycursor.execute(filter_query, (email,))
        user = mycursor.fetchone()   
        print(user,"user .................................................")     
        return {"Records :-": user}, 200    