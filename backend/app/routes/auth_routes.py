#routes/auth_routes.py

from flask import Blueprint
from app.controllers.authController import register, login, reset_password

# Create a Blueprint for the auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Register the routes with corresponding controller functions
auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/reset-password', methods=['POST'])(reset_password)
