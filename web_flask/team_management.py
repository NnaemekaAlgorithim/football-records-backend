from flask import request, jsonify, session
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from models.engine.db_engine import DBStorage
from models.player_model import Player
from models.team_model import Team
from models.user_model import User
from flask_bcrypt import Bcrypt
from web_flask.admin_management import admin_user
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker

# Initialize Bcrypt instance (assuming it's configured in app.py)
bcrypt = Bcrypt()

db_storage = DBStorage()

class CreateTeam(Resource):
    """Endpoint to create a new team.

    Endpoint: /create_team
    Method: POST

    This endpoint allows for creating a new team and saving it to the database.

    Request JSON:
        - Required: 'team_name' (string): The team's name.
        - Optional: 'team_logo' (string): The team's logo path.
        - Required: 'created_by' (string): User who created the team.
        - Required: 'updated_by' (string): User who last updated the team.

    Responses:
        201: Team created successfully.
        400: Missing JSON data or required fields.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user # can only be created by an admin
    def post(self):
        """Handle POST request to create a new team."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract team data from request
        team_name = data.get('team_name')
        team_logo = data.get('team_logo')

        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        user = db_storage.get_object_by_attribute(User, user_id=current_user_id) #retrives the user using current logged-in user ID
        if not user:
            return {'message': 'User not found'}, 404
        
        created_by = user.user_id
        updated_by = user.user_id

        # Validate required fields
        if not all([team_name, created_by, updated_by]):
            return {'message': 'Missing required fields'}, 400

        # Check if team_name already exists
        if db_storage.get_object_by_attribute(Team, team_name=team_name):
            return {'message': 'Team name already exists'}, 400

        # Create new team
        new_team = Team(
            team_name=team_name,
            team_logo=team_logo,
            created_by=created_by,
            updated_by=updated_by
        )

        # Save the new team to the database
        db_storage.add(new_team)
        db_storage.commit()

        return {'message': 'Team created successfully'}, 201

class UpdateTeam(Resource):
    """Endpoint to update an existing team.

    Endpoint: /update_team/
    Method: PUT

    This endpoint allows for updating an existing team in the database.

    Request JSON:
        - Required: 'team_id' (string): The team's ID.
        - Optional: 'team_name' (string): The team's new name.
        - Optional: 'team_logo' (string): The team's new logo path.
        - Required: 'updated_by' (string): User who last updated the team.

    Responses:
        200: Team updated successfully.
        400: Missing JSON data or required fields.
        404: Team not found.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user  # Requires admin user role
    def put(self):
        """Handle PUT request to update an existing team."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract team data from request
        team_id = data.get('team_id')
        team_name = data.get('team_name')
        team_logo = data.get('team_logo')

        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        user = db_storage.get_object_by_attribute(User, user_id=current_user_id) #retrives the user using current logged-in user ID
        if not user:
            return {'message': 'User not found'}, 404
        
        updated_by = user.user_id

        # Validate required fields
        if not all([updated_by]):
            return {'message': 'Missing required fields'}, 400

        # Retrieve the team from the database
        team = db_storage.get_object_by_attribute(Team, team_id=team_id)
        if not team:
            return {'message': 'Team not found'}, 404

        # Update team attributes if provided
        if team_name:
            team.team_name = team_name
        if team_logo:
            team.team_logo = team_logo
        team.updated_by = updated_by

        # Save the updated team to the database
        db_storage.commit()

        return {'message': 'Team updated successfully'}, 200

class GetAllTeams(Resource):
    """Endpoint to retrieve all teams.

    Endpoint: /get_all_teams
    Method: GET

    This endpoint allows for retrieving all teams from the database.

    Responses:
        200: Successfully retrieved all teams.
        404: No teams found.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def get(self):
        """Handle GET request to retrieve all teams."""
        # Retrieve all teams from the database
        teams = db_storage.get_all_objects(Team)

        # Check if any teams were found
        if not teams:
            return {'message': 'No teams found'}, 404

        # Prepare team data to return
        team_data = []
        for team in teams:
            data = {
                'team_id': team.team_id,
                'team_name': team.team_name,
                'team_logo': team.team_logo,
                'created_by': team.created_by,
                'updated_by': team.updated_by,
                'created_at': team.created_at,
                'updated_at': team.updated_at
            }
            team_data.append(data)

        return jsonify(team_data), 200

class DeleteTeam(Resource):
    """Endpoint to delete a team.

    Endpoint: /delete_team
    Method: DELETE

    This endpoint allows for deleting a team from the database.

    Request JSON:
        - Required: 'team_id' (string): The team's ID.

    Responses:
        200: Team deleted successfully.
        400: Missing JSON data or required fields.
        404: Team not found.
        403: Forbidden. Only admin users can delete teams.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user  # Requires admin user role
    def delete(self):
        """Handle DELETE request to delete a team."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract team data from request
        team_id = data.get('team_id')
        if not team_id:
            return {'message': 'Missing required fields'}, 400

        # Retrieve the team from the database
        team_to_delete = db_storage.get_object_by_attribute(Team, team_id=team_id)
        if not team_to_delete:
            return {'message': 'Team not found'}, 404

        # Delete the team from the database
        deleted = db_storage.delete_object_by_attribute(Team, team_id=team_id)
        if deleted:
            return {'message': 'Team deleted successfully'}, 200
        else:
            return {'message': 'Team deletion failed'}, 500

class GetSingleTeam(Resource):
    """Endpoint to retrieve a single team by ID.

    Endpoint: /get_team
    Method: POST

    This endpoint allows for retrieving a single team from the database by its ID provided in the JSON body.

    Request JSON:
        - Required: 'team_id' (string): The team's ID.

    Responses:
        200: Successfully retrieved the team.
        400: Missing JSON data or team_id.
        404: Team not found.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def post(self):
        """Handle POST request to retrieve a single team."""
        data = request.get_json()
        if not data or 'team_id' not in data:
            return {'message': 'Missing JSON data or team_id'}, 400

        team_id = data['team_id']

        # Retrieve the team from the database by team_id
        team = db_storage.get_object_by_attribute(Team, team_id=team_id)

        # Check if the team was found
        if not team:
            return {'message': 'Team not found'}, 404

        # Prepare team data to return
        team_data = {
            'team_id': team.team_id,
            'team_name': team.team_name,
            'team_logo': team.team_logo,
            'created_by': team.created_by,
            'updated_by': team.updated_by,
            'created_at': team.created_at,
            'updated_at': team.updated_at
        }

        return jsonify(team_data), 200
