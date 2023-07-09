from flask import Flask, jsonify, request
from flask_graphql import GraphQLView
from flask_cors import CORS
from keycloak import KeycloakOpenID
keycloak_url = 'YOUR_KEYCLOAK_URL'
realm = 'YOUR_REALM'
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

keycloak_openid = KeycloakOpenID(
    server_url=f'{keycloak_url}/auth/',
    client_id=client_id,
    realm_name=realm,
    client_secret_key=client_secret
)
def protect(view_func):
    def wrapper(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Missing token'}), 401

        try:
            userinfo = keycloak_openid.userinfo(token)
            # You can perform additional checks on userinfo if needed

            return view_func(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': str(e)}), 401

    return wrapper
import graphene

class Todo(graphene.ObjectType):
    title = graphene.String()
    description = graphene.String()
    time = graphene.String()

class Query(graphene.ObjectType):
    todos = graphene.List(Todo)

    def resolve_todos(self, info):
        # Implement logic to fetch todos from a database or any other source
        # and return them as a list of Todo objects
        pass

class Mutation(graphene.ObjectType):
    add_todo = graphene.Field(Todo, title=graphene.String(), description=graphene.String(), time=graphene.String())

    def resolve_add_todo(self, info, title, description, time):
        # Implement logic to add a new todo and return the created Todo object
        pass

schema = graphene.Schema(query=Query, mutation=Mutation)

app = Flask(__name__)
CORS(app)
@app.route('/login')
def login():
    return jsonify({'loginUrl': keycloak_openid.authorization_url('http://localhost:5000/callback')})
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = keycloak_openid.token('http://localhost:5000/callback', code)

    # You can store the token in a session or return it as a response for the client to use in subsequent requests
    return jsonify({'token': token['access_token']})
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
import graphene

class Mutation(graphene.ObjectType):
    # Existing code...

    upload_image = graphene.Field(Todo, title=graphene.String(), description=graphene.String(), time=graphene.String(), image=graphene.String())

    def resolve_upload_image(self, info, title, description, time, image):
        # Implement logic to upload the image to a storage service like AWS S3
        # and associate the image URL with the new todo
        pass
