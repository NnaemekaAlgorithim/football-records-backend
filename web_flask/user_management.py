from flask import request, jsonify, session
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from models.engine.db_engine import DBStorage
from models.user_model import User
from flask_bcrypt import Bcrypt
from web_flask.admin_management import admin_user
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker

# Initialize Bcrypt instance (assuming it's configured in app.py)
bcrypt = Bcrypt()

db_storage = DBStorage()

class RegisterUser(Resource):
    """Register a new user.

    Endpoint: /register
    Method: POST
    Requires a valid JWT token to access this endpoint and admin user permissions.

    Request JSON parameters:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        password (str): The user's password.

    Responses:
        201: Registration successful with a JWT access token.
        400: Missing JSON data or email already exists.
        404: User not found.
    """
    
    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user
    def post(self):
        """Handle POST request for registering a new user."""
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        user = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user data from request
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        created_by = user.user_id
        updated_by = user.user_id
        # Add additional required fields here

        # Check if user already exists
        existing_user = db_storage.get_object_by_attribute(User, email=email)
        if existing_user:
            return {'message': 'Email already exists, please login'}, 400

        # Hash the password before saving
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user
        user = User(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            password=hashed_password, 
            created_by=created_by, 
            updated_by=updated_by
        )
        db_storage.add(user)
        db_storage.commit()  # Commit changes to the database

        # Generate JWT token
        access_token = create_access_token(identity=email)
        return {'message': 'Registration successful', 'access_token': access_token}, 201

class LoginUser(Resource):
    """Login a user.

    Endpoint: /login
    Method: POST

    Request JSON parameters:
        email (str): The user's email address.
        password (str): The user's password.

    Responses:
        200: Login successful with a JWT access token.
        400: Missing JSON data.
        401: Invalid email or password.
    """
    
    def post(self):
        """Handle POST request for user login."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user data from request
        email = data.get('email')
        password = data.get('password')

        # Check if user exists
        user = db_storage.get_object_by_attribute(User, email=email)
        if not user:
            return {'message': 'Invalid email'}, 401

        # Verify password hash
        if not bcrypt.check_password_hash(user.password, password):
            return {'message': 'Invalid password'}, 401

        # Login successful, generate access token
        access_token = create_access_token(identity=user.user_id)  # Use user ID for identity

        return {'message': 'Login successful', 'access_token': access_token}, 200

class UserProfile(Resource):
    """Fetch user profile details.

    Endpoint: /profile
    Method: GET

    This endpoint requires a valid JWT token.

    Responses:
        200: User profile details in JSON format.
        404: User not found.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def get(self):
        """Handle GET request to fetch user profile details."""
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        # Retrieve the user from the database using the user_id
        user = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user:
            return {'message': 'User not found'}, 404

        # Return the user's profile details, excluding the password
        user_profile = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'created_by': user.created_by,
            'updated_by': user.updated_by
        }

        return jsonify(user_profile)

class AllUserProfile(Resource):
    """Fetch all user profiles.

    Endpoint: /all_profiles
    Method: GET

    This endpoint requires a valid JWT token and admin user role.

    Responses:
        200: List of all user profiles in JSON format.
        403: User is not authorized to access this endpoint.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user  # Requires admin user role (replace with your admin check)
    def get(self):
        """Handle GET request to fetch all user profiles."""
        # Retrieve all the users from the database
        users = db_storage.get_all_objects(User)

        user_data = []
        # Collect profile details for each user, excluding the password
        for user in users:
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'created_by': user.created_by,
                'updated_by': user.updated_by
            }
            user_data.append(data)
        return jsonify(user_data)

class UpdateUser(Resource):
    """Update user profile details.

    Endpoint: /update_profile
    Method: PATCH

    This endpoint requires a valid JWT token.

    Request JSON:
        - Optional: 'first_name' (string)
        - Optional: 'last_name' (string)
        - Optional: 'email' (string)
        - Optional: 'password' (string) along with 'previous_password' (string) for validation

    Responses:
        200: User updated successfully.
        400: Missing JSON data or no fields to update.
        401: Incorrect previous password.
        404: User not found.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    def patch(self):
        """Handle PATCH request to update user profile."""
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        # Retrieve JSON data from the request
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Ensure at least one data field is provided (excluding password)
        data_to_update = {field: value for field, value in data.items() if field != 'previous_password'}
        if not data_to_update:
            return {'message': 'No fields to update'}, 400

        # Retrieve the user from the database
        user_to_update = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user_to_update:
            return {'message': 'User not found'}, 404

        # Validate previous password before updating password
        if 'password' in data:
            old_password = data.get('previous_password')  # Assuming 'previous_password' key is sent
            if not old_password or not bcrypt.check_password_hash(user_to_update.password, old_password):
                return {'message': 'Incorrect previous password'}, 401

        # Update the user fields (excluding password if not provided)
        for field, value in data_to_update.items():
            setattr(user_to_update, field, value)

        # Hash the new password if it is being updated
        if 'password' in data:
            user_to_update.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Save the updated user to the database
        db_storage.add(user_to_update)
        db_storage.commit()

        return {'message': 'User updated successfully'}, 200

class DeleteUser(Resource):
    """Delete a user from the system.

    Endpoint: /delete_user
    Method: DELETE

    This endpoint requires a valid JWT token and admin user role.

    Request JSON:
        - Required: 'email' (string) - Email of the user to be deleted

    Responses:
        200: User deleted successfully.
        400: Missing JSON data or email.
        404: User not found or unauthorized action.
        500: User deletion failed.
    """

    @jwt_required()  # Requires a valid JWT token to access this endpoint
    @admin_user  # Requires admin user role (replace with your admin check)
    def delete(self):
        """Handle DELETE request to delete a user."""
        current_user_id = get_jwt_identity()  # Get the current logged-in user ID

        # Retrieve JSON data from the request
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user email from the request
        email = data.get('email')
        if not email:
            return {'message': 'Missing email'}, 400

        # Check if user exists
        user_to_delete = db_storage.get_object_by_attribute(User, email=email)
        if not user_to_delete:
            return {'message': 'User not found'}, 404

        # Check if the current user is an admin
        user = db_storage.get_object_by_attribute(User, user_id=current_user_id)
        if not user.admin:
            return {'message': 'You must be an admin to perform this action'}, 404

        # Delete the user (admin authorized deletion)
        deleted = db_storage.delete_object_by_attribute(User, email=email)
        if deleted:
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User deletion failed'}, 500

class AdminUserFirstLogin(Resource):
    """Handle the first login for admin users.

    Endpoint: /admin_first_login
    Method: POST

    This endpoint allows an admin user to log in for the first time and update their password.

    Request JSON:
        - Required: 'email' (string) - The email of the user.
        - Required: 'password' (string) - The current password of the user.
        - Optional: 'new_password' (string) - The new password for admin users to set.

    Responses:
        200: Login successful with access token.
        400: Missing JSON data.
        401: Invalid email or password.
    """

    def post(self):
        """Handle POST request to log in an admin user for the first time."""
        data = request.get_json()
        if not data:
            return {'message': 'Missing JSON data'}, 400

        # Extract user data from request (including new password for admins)
        email = data.get('email')
        password = data.get('password')
        new_password = data.get('new_password')  # New field for admin password reset

        # Check if user exists
        user = db_storage.get_object_by_attribute(User, email=email)
        if not user:
            return {'message': 'Invalid email or password'}, 401

        # Verify password hash (skip if admin and new_password provided)
        if not (user.admin and new_password):  # Check for admin and new password
            if not bcrypt.check_password_hash(user.password, password):
                return {'message': 'Invalid email or password'}, 401

        # Update password if admin and new_password provided
        if user.admin and new_password:
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db_storage.add(user)
            db_storage.commit()  # Save the updated password

        # Login successful, generate access token
        access_token = create_access_token(identity=user.user_id)  # Use user ID for identity

        return {'message': 'Login successful', 'access_token': access_token}, 200
