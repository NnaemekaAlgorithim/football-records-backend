from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
import secrets
from web_flask.user_management import AllUserProfile, RegisterUser, LoginUser, AdminUserFirstLogin
from web_flask.user_management import UserProfile, UpdateUser, DeleteUser
from web_flask.player_management import CreatePlayer, UpdatePlayer, UpdatePlayerSubscription
from web_flask.player_management import GetAllPlayers, GetSinglePlayer, DeletePlayer
from web_flask.team_management import CreateTeam, UpdateTeam, DeleteTeam,
from web_flask.team_management import GetAllTeams, GetSingleTeam
from flask import Flask, redirect, url_for
from flask_redoc import Redoc

# Create a Flask app
app = Flask(__name__)
CORS(app)

# Set the secret key for Flask sessions
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Set the secret key for JWT tokens
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
jwt = JWTManager(app)

# Create an API instance
api = Api(app)

# Register the registration and login resources with the API
api.add_resource(RegisterUser, '/register')
api.add_resource(LoginUser, '/login')
api.add_resource(AdminUserFirstLogin, '/admin_first_login')
api.add_resource(UserProfile, "/user_profile")
api.add_resource(UpdateUser, '/update_user')
api.add_resource(AllUserProfile, '/all_users')
api.add_resource(DeleteUser, '/delete_user')
api.add_resource(CreatePlayer, '/create_player')
api.add_resource(UpdatePlayer, '/update_player')
api.add_resource(UpdatePlayerSubscription, '/update_player_subscription')
api.add_resource(GetAllPlayers, '/get_all_players')
api.add_resource(GetSinglePlayer, '/get_single_player')
api.add_resource(DeletePlayer, '/delete_player')
api.add_resource(CreateTeam, '/create_team')
api.add_resource(UpdateTeam, '/update_team')
api.add_resource(DeleteTeam, '/delete_team')
api.add_resource(GetSingleTeam, '/get_single_team')
api.add_resource(GetAllTeams, '/get_all_teams')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
