# backend/app/controllers/auth_controller.py

from flask import request, jsonify
from app.services.user_service import register_user, authenticate_user, update_password
from app.utils.jwt_util import generate_jwt

# Register User
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'All fields are required.'}), 400

    success, message = register_user(username, email, password)
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'error': message}), 400

# Login User
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Email and password are required.'}), 400

    user = authenticate_user(email, password)
    if user:
        token = generate_jwt(user["id"])
        return jsonify({
            'message': 'Login successful.',
            'user_id': user["id"],
            'token': token
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials.'}), 401

# Reset Password
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if not all([email, new_password]):
        return jsonify({'error': 'Email and new password are required.'}), 400

    success, message = update_password(email, new_password)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400
