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
from models.player_stats_model import PlayerStats

# Initialize Bcrypt instance (assuming it's configured in app.py)
bcrypt = Bcrypt()

db_storage = DBStorage()

class CreatePlayerStats(Resource):
    """Endpoint to create a new player stats entry.

    Endpoint: /create_player_stats
    Method: POST

    This endpoint allows for creating new player stats and saving them to the database.

    Request JSON:
        - Required: 'player_id' (string): The ID of the player.
        - Required: 'current_team' (string): The name of the current team.
        - Optional: 'previous_team' (string): The name of the player's previous team.
        - Optional: 'joined_team_at' (string): When the player joined the team.
        - Optional: 'left_team_at' (string): When the player left the team.
        - Optional: 'season_played' (string): The season the statistics were recorded.
        - Optional: 'match_half_played' (string): The match half played.
        - Required: 'start_match' (boolean): Whether the player started the match.
        - Optional: 'sub_in_at' (string): The time the player was substituted in.
        - Optional: 'sub_out_at' (string): The time the player was substituted out.
        - Required: 'opposing_team' (string): The opposing team.
        - Required: 'match_type' (string): The type of match.
        - Optional stats fields (integer): Control, pass, duel, dribble, cross, shoot, interception, pass, tackle, clearance, foul, corner, free kick, penalty kick, card, save, concede, offside, goal, assist, throw-in stats.
        - Required: 'created_by' (string): User who created the data.
        - Required: 'updated_by' (string): User who updated the data.

    Responses:
        201: Player stats created successfully.
        400: Missing JSON data or required fields.
    """
    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def post(self):
        """Handle POST request to create a new player stats entry."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract required data from request
        player_id = data.get('player_id')
        current_team = data.get('current_team')
        start_match = data.get('start_match')
        opposing_team = data.get('opposing_team')
        match_type = data.get('match_type')

        current_user_id = get_jwt_identity()  # Get the current logged-in user ID
        user = db_storage.get_object_by_attribute(User, user_id=current_user_id)  # Retrieve the user using current logged-in user ID
        if not user:
            return {'message': 'User not found'}, 404
        
        created_by = user.user_id
        updated_by = user.user_id

        # Validate required fields
        if not all([player_id, current_team, start_match, opposing_team, match_type, created_by, updated_by]):
            return {'message': 'Missing required fields'}, 400

        # Create new player stats entry
        new_player_stats = PlayerStats(
            player_id=player_id,
            current_team=current_team,
            previous_team=data.get('previous_team'),
            joined_team_at=data.get('joined_team_at'),
            left_team_at=data.get('left_team_at'),
            season_played=data.get('season_played'),
            match_half_played=data.get('match_half_played'),
            start_match=start_match,
            sub_in_at=data.get('sub_in_at'),
            sub_out_at=data.get('sub_out_at'),
            opposing_team=opposing_team,
            match_type=match_type,
            control_success=data.get('control_success', 0),
            control_fail=data.get('control_fail', 0),
            short_pass_success=data.get('short_pass_success', 0),
            short_pass_fail=data.get('short_pass_fail', 0),
            duel_success=data.get('duel_success', 0),
            duel_fail=data.get('duel_fail', 0),
            long_pass_success=data.get('long_pass_success', 0),
            long_pass_fail=data.get('long_pass_fail', 0),
            dribble_success=data.get('dribble_success', 0),
            dribble_fail=data.get('dribble_fail', 0),
            cross_success=data.get('cross_success', 0),
            cross_fail=data.get('cross_fail', 0),
            shoot_success=data.get('shoot_success', 0),
            shoot_fail=data.get('shoot_fail', 0),
            interception_success=data.get('interception_success', 0),
            interception_fail=data.get('interception_fail', 0),
            one_touch_pass_success=data.get('one_touch_pass_success', 0),
            one_touch_pass_fail=data.get('one_touch_pass_fail', 0),
            call_of_ball_success=data.get('call_of_ball_success', 0),
            call_of_ball_fail=data.get('call_of_ball_fail', 0),
            tackle_success=data.get('tackle_success', 0),
            tackle_fail=data.get('tackle_fail', 0),
            clearance_success=data.get('clearance_success', 0),
            clearance_fail=data.get('clearance_fail', 0),
            fouled_on=data.get('fouled_on', 0),
            foul_commited=data.get('foul_commited', 0),
            corner_success=data.get('corner_success', 0),
            corner_fail=data.get('corner_fail', 0),
            free_kick_success=data.get('free_kick_success', 0),
            free_kick_fail=data.get('free_kick_fail', 0),
            penalty_kick_success=data.get('penalty_kick_success', 0),
            penalty_kick_fail=data.get('penalty_kick_fail', 0),
            yellow_card=data.get('yellow_card', 0),
            red_card=data.get('red_card', 0),
            goal_save=data.get('goal_save', 0),
            goal_conceded=data.get('goal_conceded', 0),
            penalty_save=data.get('penalty_save', 0),
            penalty_conceded=data.get('penalty_conceded', 0),
            offside=data.get('offside', 0),
            goal_scored=data.get('goal_scored', 0),
            assists=data.get('assists', 0),
            throw_in_success=data.get('throw_in_success', 0),
            throw_in_fail=data.get('throw_in_fail', 0),
            created_by=created_by,
            updated_by=updated_by
        )

        # Save the new player stats to the database
        db_storage.add(new_player_stats)
        db_storage.commit()

        return {'message': 'Player stats created successfully'}, 201
    
class GetPlayerStats(Resource):
    """Endpoint to retrieve all player stats for a given player ID.

    Endpoint: /get_player_stats
    Method: POST

    This endpoint allows for retrieving all player stats for a specified player from the database.

    Request JSON:
        - Required: 'player_id' (string): The ID of the player.

    Responses:
        200: Successfully retrieved player stats.
        400: Missing JSON data or required fields.
        404: No player stats found.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def post(self):
        """Handle POST request to retrieve player stats."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract player ID from request
        player_id = data.get('player_id')
        if not player_id:
            return {'message': 'Missing required field: player_id'}, 400

        # Retrieve player stats from the database by player ID
        player_stats = db_storage.get_object_by_attribute(PlayerStats, player_id=player_id)

        # Retrieve a particular player from database.
        player = db_storage.get_object_by_attribute(Player, player_id=player_id)

        if not player.subcribed:
            return {'message': 'Player is not subscribed'}, 200

        # Check if any player stats were found
        if not player_stats:
            return {'message': 'No player stats found for the given player_id'}, 404

        # Prepare player stats data to return
        stats_data = []
        for stats in player_stats:
            data = {
                'stat_id': stats.stat_id,
                'player_id': stats.player_id,
                'current_team': stats.current_team,
                'previous_team': stats.previous_team,
                'joined_team_at': stats.joined_team_at,
                'left_team_at': stats.left_team_at,
                'season_played': stats.season_played,
                'match_half_played': stats.match_half_played,
                'start_match': stats.start_match,
                'sub_in_at': stats.sub_in_at,
                'sub_out_at': stats.sub_out_at,
                'opposing_team': stats.opposing_team,
                'match_type': stats.match_type,
                'control_success': stats.control_success,
                'control_fail': stats.control_fail,
                'short_pass_success': stats.short_pass_success,
                'short_pass_fail': stats.short_pass_fail,
                'duel_success': stats.duel_success,
                'duel_fail': stats.duel_fail,
                'long_pass_success': stats.long_pass_success,
                'long_pass_fail': stats.long_pass_fail,
                'dribble_success': stats.dribble_success,
                'dribble_fail': stats.dribble_fail,
                'cross_success': stats.cross_success,
                'cross_fail': stats.cross_fail,
                'shoot_success': stats.shoot_success,
                'shoot_fail': stats.shoot_fail,
                'interception_success': stats.interception_success,
                'interception_fail': stats.interception_fail,
                'one_touch_pass_success': stats.one_touch_pass_success,
                'one_touch_pass_fail': stats.one_touch_pass_fail,
                'call_of_ball_success': stats.call_of_ball_success,
                'call_of_ball_fail': stats.call_of_ball_fail,
                'tackle_success': stats.tackle_success,
                'tackle_fail': stats.tackle_fail,
                'clearance_success': stats.clearance_success,
                'clearance_fail': stats.clearance_fail,
                'fouled_on': stats.fouled_on,
                'foul_commited': stats.foul_commited,
                'corner_success': stats.corner_success,
                'corner_fail': stats.corner_fail,
                'free_kick_success': stats.free_kick_success,
                'free_kick_fail': stats.free_kick_fail,
                'penalty_kick_success': stats.penalty_kick_success,
                'penalty_kick_fail': stats.penalty_kick_fail,
                'yellow_card': stats.yellow_card,
                'red_card': stats.red_card,
                'goal_save': stats.goal_save,
                'goal_conceded': stats.goal_conceded,
                'penalty_save': stats.penalty_save,
                'penalty_conceded': stats.penalty_conceded,
                'offside': stats.offside,
                'goal_scored': stats.goal_scored,
                'assists': stats.assists,
                'throw_in_success': stats.throw_in_success,
                'throw_in_fail': stats.throw_in_fail,
                'created_by': stats.created_by,
                'updated_by': stats.updated_by,
                'created_at': stats.created_at,
                'updated_at': stats.updated_at
            }
            stats_data.append(data)

        return jsonify(stats_data), 200
