from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify, make_response
from genopaths.modules.users.models import User, UserSchema
from genopaths.extensions import db
from genopaths import app
import datetime
from flask_login import login_required, login_manager
from datetime import datetime
import base64
from sqlalchemy import or_
from sqlalchemy.dialects import postgresql

mod_users = Blueprint('users', __name__, url_prefix='/api/users')


@mod_users.route('/', methods=['GET'])
@login_required
def get_users():
    """Get a list of all the users in the system"""
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    other_names = request.args.get('other_names')
    username = request.args.get('username')
    job_title = request.args.get('job_title')
    role = request.args.get('role')
    phone_number = request.args.get('phone_number')

    ma_schema = UserSchema()
    query = User.query
    
    filter_params = {}
    if first_name: query = query.filter(User.first_name.like('%{}%'.format(first_name)))
    if last_name: query = query.filter(User.last_name.like('%{}%'.format(last_name)))
    if other_names: query = query.filter(User.other_names.like('%{}%'.format(other_names)))
    if job_title: query = query.filter(User.job_title.like('%{}%'.format(job_title)))
    if role: query = query.filter_by(role=role)
    if phone_number: query = query.filter(User.phone_number.like('%{}%'.format(phone_number)))
    
    #query.filter_by(first_name=first_name)
    #if bool(filter_params): query.filter_by(or_(False, **filter_params))
    statement = query.statement
    app.logger.info(statement.compile(dialect=postgresql.dialect()))
    return jsonify({
        'status': 'success',
        'data': [ma_schema.dump(v) for v in query.all()] 
    })


@mod_users.route('/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    """Get vendor details"""

    ma_schema = UserSchema()

    return jsonify(ma_schema.dump(User.query.get(id)).data)


@mod_users.route('/<int:id>', methods=['POST','PUT'])
@login_required
def update_user(id):
    """Update user details"""
    content = request.get_json()
    user = User.query.filter_by(pk=id).first()

    # @TODO: Throw exception if an attempt to change the username/email is made here

    if "first_name" in content: user.first_name = content['first_name']
    if "last_name" in content: user.last_name = content['last_name']
    if "other_names" in content: user.other_names = content['other_names']
    if "phone_number" in content: user.phone_number = content['phone_number']
    if "photo" in content: user.photo = content['photo']
    if "job_title" in content: user.job_title = content['job_title']
    if "role" in content: user.role = content['role']

    db.session.commit()

    return jsonify({"status": "success"})


@mod_users.route('', methods=['DELETE'])
@login_required
def delete_users():
    """Delete users"""
    content = request.get_json()
    pks = content['pks']

    deleted_objects = User.__table__.delete().where(User.pk.in_(pks))
    db.session.execute(deleted_objects)
    db.session.commit()

    return jsonify({"status":"success"})

@mod_users.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    """Delete user"""
    User.query.filter_by(pk=id).delete()

    db.session.commit()

    return jsonify({"status":"OK"})

@mod_users.route('/', methods=['POST'])
@login_required
def add_user():
    """Add a user"""
    content = request.get_json()

    if content['password'] != content['password2']:
        return jsonify({"status": 'error', "message": 'Passwords donot much.' })
        
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    app.logger.info(timestamp)
    token = base64.b64encode(bytes(str(timestamp) + content['username'], 'utf-8')).decode("utf-8")

    other_names = "" if content['other_names'] is None else content['other_names']
    user = User(username=content['username'],
                first_name=content['first_name'],
                last_name=content['last_name'],
                other_names=content['other_names'],
                phone_number=content['phone_number'],
                job_title=content['job_title'],
                is_account_non_expired=False,
                is_account_non_locked=True,
                is_enabled=True,
                password=content['password'],
                role=content['role'],
                token=token,
                photo="",)

    db.session.add(user)
    db.session.commit()

    return jsonify({"status":"success", "message": 'User registered successfully'})
    
@mod_users.route('/currentuser', methods=['GET'])
@login_required
def get_currentuser():
    ma_schema = UserSchema()

    token = request.headers.get('Authorization')
    token = token.replace('Bearer ', '', 1)
    user = User.query.filter_by(token=token).first()

    app.logger.info("token:" + token)
    
    return jsonify({
        'status': 'success',
        'data': ma_schema.dump(user)
    })