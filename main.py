
from login import signup_namespace, Login, app, api,  TokenRefresh, GetRecord
from signup import signup_namespace, Signup

# Add the namespaces and resources to the API
api.add_namespace(signup_namespace)
api.add_resource(Signup, '/signup')

api.add_namespace(signup_namespace)
api.add_resource(Login, '/login')

api.add_namespace(signup_namespace)
api.add_resource(TokenRefresh, '/refresh-token')

api.add_namespace(signup_namespace)
api.add_resource(GetRecord, '/get-record')


if __name__ == '__main__':
    app.run(debug=True)


