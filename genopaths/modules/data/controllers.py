from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify, make_response
from genopaths.modules.parameters.models import Data, DataSchema
from genopaths.extensions import db
from genopaths import app
import datetime
from flask_login import login_required, login_manager
from datetime import datetime
import base64
from sqlalchemy import or_
from sqlalchemy.dialects import postgresql

mod_parameters = Blueprint('data', __name__, url_prefix='/api/data')

@mod_data.route('/', methods=['GET'])
@login_required
def get_data():
    """Get a list of all the data"""
    name = request.args.get('name')
    
    ma_schema = ParameterSchema()
    query = Parameter.query

    if name: query = query.filter(Parameter.name.like('%{}%'.format(name)))
    
    return jsonify({
        'status': 'success',
        'data': [ma_schema.dump(v) for v in query.all()] 
    })


@mod_parameters.route('/<int:id>', methods=['GET'])
@login_required
def get_parameter(id):
    """Get parameter details"""

    ma_schema = ParameterSchema()

    return jsonify({'status': 'success', 'data': ma_schema.dump(Parameter.query.get(id))})

@mod_parameters.route('', methods=['DELETE'])
@login_required
def delete_users():
    """Delete parameters"""
    content = request.get_json()
    pks = content['ids']

    deleted_objects = Parameter.__table__.delete().where(Parameter.id.in_(ids))
    db.session.execute(deleted_objects)
    db.session.commit()

    return jsonify({"status":"success"})

@mod_parameters.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_parameter(id):
    """Delete parameter"""
    Parameter.query.filter_by(id=id).delete()

    db.session.commit()

    return jsonify({"status":"OK"})

@mod_parameters.route('/', methods=['POST'])
@login_required
def add_parameter():
    """Add a parameter"""
    content = request.get_json()

    parameter = Parameter(
                name=content['name'],
                label=content['label'],
                description=content['description'],
                validation=content['validation'],
                required=content['required'],
                project_id=content['project_id'],
                created_by=g.currentuser.id,
                updated_by=g.currentuser.id
            )

    db.session.add(parameter)
    db.session.commit()

    return jsonify({"status":"success", "message": 'Parameter added successfully'})


@mod_parameters.route('/<int:id>', methods=['POST','PUT', 'PATCH'])
@login_required
def update_parameters(id):
    """Update project prameters details"""
    content = request.get_json()
    parameter = Parameter.query.filter_by(id=id).first()

    if "name" in content: parameter.name = content['name']
    if "label" in content: parameter.label = content['label']
    if "description" in content: parameter.description = content['description']
    if "type" in content: parameter.type = content['type']
    if "validation" in content: parameter.validation = content['validation']
    if "required" in content: parameter.required = content['required']

    db.session.commit()

    return jsonify({"status": "success"})