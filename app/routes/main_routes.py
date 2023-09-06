import logging
import os
from functools import wraps
from flask import Blueprint, jsonify, make_response, render_template, request
from flask_jwt_extended import decode_token, get_jwt_identity
from app.Models.UserModel import User

main = Blueprint('main', __name__)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = decode_token(token)
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


@main.route('/')
def home():
    resp = make_response(render_template('layout.html'))
    # Modify resp here if needed, e.g., set a cookie
    return resp, 200


@main.route('/debug')
def debug_route():
    template_folder_path = os.path.join(os.getcwd(), '../templates')
    return f"Template folder path: {template_folder_path}"


@main.route('/admin', methods=['GET'])
@token_required
def admin_route():
    current_user_id = get_jwt_identity()
    print(current_user_id)
    user = User.find_by_id(current_user_id)

    if not user.has_role('admin'):
        logging.warning(f'Unauthorized access attempt by: {current_user_id}')
        logging.info({'message': 'You do not have permission to access this route'}), 403

    logging.info({'message': 'This is an admin route'})
