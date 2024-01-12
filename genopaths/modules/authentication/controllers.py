from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify, make_response
from genopaths.modules.users.models import User, UserSchema
from genopaths.extensions import db
from genopaths import app
import datetime
import base64
from datetime import datetime

# @TODO: Change this endpoint to /api/authentication
mod_auth = Blueprint('authetication', __name__, url_prefix='/api/auth')


@mod_auth.route('/login', methods=['POST'])
def authenticate_user():
    """Authenticate user"""
    content = request.get_json()
    username = content['username']
    password = content['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user is not None:
        ma_schema = UserSchema()
        user_data = ma_schema.dump(user)
        user_data['id'] = user.id
        user_data['token'] = user.token #base64.b64encode(bytes(user.token, 'utf-8')).decode("utf-8")

        del user_data['id']

        return jsonify({'status':'success', 'data':user_data})
    else:
        return jsonify({'status':'fail','message': 'User authentication failed'})


@mod_auth.route('/register', methods=['POST'])
def register_user():
    """Authenticate user"""
    
    content = request.get_json()
    app.logger.info(content)
    #check password 
    if content['password'] != content['confirm_password']:
        return jsonify({"status": 'error', "message": 'Passwords donot much.' })

    now = datetime.now()
    timestamp = datetime.timestamp(now)
    app.logger.info(timestamp)
    token = base64.b64encode(bytes(str(timestamp), 'utf-8')).decode("utf-8")
    
    user = User(username=content['username'],
                first_name=content['first_name'],
                role=content['role'],
                last_name=content['last_name'],
                other_names=content['other_names'],
                password=content['password'],
                phone_number=content['phone_number'],
                job_title=content['job_title'],
                is_account_non_expired= True, #content['is_account_non_expired'],
                is_account_non_locked= True, #content['is_account_non_locked'],
                is_enabled=True, #content['is_enabled'],
                token=token,
                photo=content['photo'] if 'photo' in content else None
                )

    db.session.add(user)
    db.session.commit()

    return jsonify({"status":"success", "message": 'User registered successfully'})

