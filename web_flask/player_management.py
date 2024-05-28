from flask import request, jsonify, session
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from models.engine.db_engine import DBStorage
from models.player_model import Player
from models.user_model import User
from flask_bcrypt import Bcrypt
from web_flask.admin_management import admin_user
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker

# Initialize Bcrypt instance (assuming it's configured in app.py)
bcrypt = Bcrypt()

db_storage = DBStorage()

class CreatePlayer(Resource):
    """Endpoint to create a new player.

    Endpoint: /create_player
    Method: POST

    This endpoint allows for creating a new player and saving them to the database.

    Request JSON:
        - Required: 'player_first_name' (string): The player's first name.
        - Required: 'player_last_name' (string): The player's last name.
        - Required: 'player_age' (integer): The player's age.
        - Required: 'player_team' (string): The ID of the team the player belongs to.
        - Optional: 'player_image' (string): The player's image path.
        - Required: 'player_height' (integer): The player's height in centimeters.
        - Required: 'player_primary_position' (string): The player's primary position.
        - Optional: 'subscribed' (boolean): Indicates if a player is subscribed. Default is False.
        - Required: 'created_by' (string): User who created the player.
        - Required: 'updated_by' (string): User who last updated the player.

    Responses:
        201: Player created successfully.
        400: Missing JSON data or required fields.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def post(self):
        """Handle POST request to create a new player."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract player data from request
        player_first_name = data.get('player_first_name')
        player_last_name = data.get('player_last_name')
        player_age = data.get('player_age')
        player_team = data.get('player_team')
        player_image = data.get('player_image')
        player_height = data.get('player_height')
        player_primary_position = data.get('player_primary_position')

        subscribed = False #set subscribed to false by default

        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        user = db_storage.get_object_by_attribute(User, user_id=current_user_id) #retrives the user using current logged-in user ID
        if not user:
            return {'message': 'User not found'}, 404
        
        created_by = user.user_id
        updated_by = user.user_id

        # Validate required fields
        if not all([player_first_name, player_last_name, player_age, player_team, player_height, player_primary_position, created_by, updated_by]):
            return {'message': 'Missing required fields'}, 400

        # Create new player
        new_player = Player(
            player_first_name=player_first_name,
            player_last_name=player_last_name,
            player_age=player_age,
            player_team=player_team,
            player_image=player_image,
            player_height=player_height,
            player_primary_position=player_primary_position,
            subscribed=subscribed,
            created_by=created_by,
            updated_by=updated_by
        )

        # Save the new player to the database
        db_storage.add(new_player)
        db_storage.commit()

        return {'message': 'Player created successfully'}, 201

class UpdatePlayer(Resource):
    """Endpoint to update a player.

    Endpoint: /update_player/<string:player_id>
    Method: PATCH

    This endpoint allows for updating an existing player, excluding the subscribed attribute.

    Request JSON:
        - Optional: 'player_first_name' (string): The player's first name.
        - Optional: 'player_last_name' (string): The player's last name.
        - Optional: 'player_age' (integer): The player's age.
        - Optional: 'player_team' (string): The ID of the team the player belongs to.
        - Optional: 'player_image' (string): The player's image path.
        - Optional: 'player_height' (integer): The player's height in centimeters.
        - Optional: 'player_primary_position' (string): The player's primary position.

    Responses:
        200: Player updated successfully.
        400: Missing JSON data or required fields.
        404: Player not found.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def patch(self):
        """Handle PATCH request to update an existing player."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400
        
        player_id = data.get('player_id')

        # Retrieve the player from the database
        player_to_update = db_storage.get_object_by_attribute(Player, player_id=player_id)
        if not player_to_update:
            return {'message': 'Player not found'}, 404

        # Update the player fields
        for field in ['player_first_name', 'player_last_name', 'player_age', 'player_team', 'player_image', 'player_height', 'player_primary_position']:
            if field in data:
                setattr(player_to_update, field, data[field])

        # Update the updated_by field
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID
        user = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        player_to_update.updated_by = user.user_id

        # Save the updated player to the database
        db_storage.add(player_to_update)
        db_storage.commit()

        return {'message': 'Player updated successfully'}, 200

class UpdatePlayerSubscription(Resource):
    """Endpoint to update a player's subscription status.

    Endpoint: /update_player_subscription/
    Method: PATCH

    This endpoint allows for updating the subscribed status of an existing player, and can only be accessed by an admin.

    Request JSON:
        - Required: 'subscribed' (boolean): The new subscription status.
        - Required: 'player_id' (string): The player_id to update.

    Responses:
        200: Subscription status updated successfully.
        400: Missing JSON data or required fields.
        404: Player not found.
        403: Unauthorized, only admins can perform this action.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user  # Requires admin user role (replace with your admin check)
    def patch(self):
        """Handle PATCH request to update an existing player's subscription status."""
        data = request.get_json()
        if not data or 'subscribed' not in data or 'player_id' not in data:
            return {'message': 'Missing JSON data or required fields'}, 400
        
        player_id = data.get('player_id')

        # Retrieve the player from the database
        player_to_update = db_storage.get_object_by_attribute(Player, player_id=player_id)
        if not player_to_update:
            return {'message': 'Player not found'}, 404

        # Update the subscribed status
        player_to_update.subscribed = data['subscribed']

        # Save the updated player to the database
        db_storage.add(player_to_update)
        db_storage.commit()

        return {'message': 'Subscription status updated successfully'}, 200

class GetAllPlayers(Resource):
    """Endpoint to retrieve all players.

    Endpoint: /get_all_players
    Method: GET

    This endpoint allows for retrieving all subscribed players from the database.

    Responses:
        200: Returns a list of subscribed players.
        500: Internal server error.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def get(self):
        """Handle GET request to retrieve all subscribed players."""
        try:
            # Retrieve all subscribed players from the database
            players = db_storage.get_all_objects(Player)

            # Prepare player data for response, excluding unsubscribed players
            player_data = []
            for player in players:
                if player.subscribed:
                    data = {
                        'player_id': player.player_id,
                        'player_first_name': player.player_first_name,
                        'player_last_name': player.player_last_name,
                        'player_age': player.player_age,
                        'player_team': player.player_team,
                        'player_image': player.player_image,
                        'player_height': player.player_height,
                        'player_primary_position': player.player_primary_position,
                        'subscribed': player.subscribed,
                        'created_by': player.created_by,
                        'updated_by': player.updated_by,
                        'created_at': player.created_at,
                        'updated_at': player.updated_at
                    }
                    player_data.append(data)
                
            return jsonify(player_data), 200
        except Exception as e:
            return {'message': 'Internal server error', 'error': str(e)}, 500

class GetSinglePlayer(Resource):
    """Endpoint to retrieve a single player.

    Endpoint: /get_player/<string:player_id>
    Method: GET

    This endpoint allows for retrieving a single player from the database by player ID.

    Responses:
        200: Returns the player data if subscribed, else returns message indicating unsubscribed.
        404: Player not found.
        500: Internal server error.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def get(self):
        """Handle GET request to retrieve a single player."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data or required fields'}, 400
        
        player_id = data.get('player_id')

        try:
            # Retrieve the player from the database
            player = db_storage.get_object_by_attribute(Player, player_id=player_id)
            if not player:
                return {'message': 'Player not found'}, 404

            # Check if player is subscribed
            if not player.subscribed:
                return {'message': 'Player is unsubscribed'}, 200

            # Prepare player data for response
            player_data = {
                'player_id': player.player_id,
                'player_first_name': player.player_first_name,
                'player_last_name': player.player_last_name,
                'player_age': player.player_age,
                'player_team': player.player_team,
                'player_image': player.player_image,
                'player_height': player.player_height,
                'player_primary_position': player.player_primary_position,
                'subscribed': player.subscribed,
                'created_by': player.created_by,
                'updated_by': player.updated_by,
                'created_at': player.created_at,
                'updated_at': player.updated_at
            }

            return jsonify(player_data), 200
        except Exception as e:
            return {'message': 'Internal server error', 'error': str(e)}, 500

class DeletePlayer(Resource):
    """Endpoint to delete a player.

    Endpoint: /delete_player/
    Method: DELETE

    Request JSON:
        - Required: 'player_id' (string): The player ID to delete..

    This endpoint allows for deleting a player from the database by player ID.
    Requires admin user role.

    Responses:
        200: Player deleted successfully.
        404: Player not found.
        401: Unauthorized access.
        500: Internal server error.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user  # Requires admin user role (replace with your admin check)
    def delete(self):
        """Handle DELETE request to delete a single player."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data or required fields'}, 400
        
        player_id = data.get('player_id')

        try:
            # Retrieve the player from the database
            player = db_storage.get_object_by_attribute(Player, player_id=player_id)
            if not player:
                return {'message': 'Player not found'}, 404

            # Delete the player
            deleted = db_storage.delete_object_by_attribute(Player, player_id=player_id)
            if deleted:
                return {'message': 'Player deleted successfully'}, 200
            else:
                return {'message': 'Player deletion failed'}, 500
        except Exception as e:
            return {'message': 'Internal server error', 'error': str(e)}, 500
