from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify, make_response
from genopaths.modules.projects.models import Project, ProjectSchema
from genopaths.extensions import db
from genopaths import app
import datetime
from flask_login import login_required, login_manager
from datetime import datetime
import base64
from sqlalchemy import or_
from sqlalchemy.dialects import postgresql

mod_projects = Blueprint('projects', __name__, url_prefix='/api/projects')

@mod_projects.route('/projects', methods=['GET'])
@login_required
def get_network_entities():
    """Get a list of all the projects"""
    name = request.args.get('name')
    
    ma_schema = ProjectSchema()
    query = Project.query

    if name: query = query.filter(Project.name.like('%{}%'.format(name)))
    
    return jsonify({
        'status': 'success',
        'data': [ma_schema.dump(v) for v in query.all()] 
    })


@mod_projects.route('/<int:id>', methods=['GET'])
@login_required
def get_project(id):
    """Get project details"""

    ma_schema = ProjectSchema()

    return jsonify(ma_schema.dump(Project.query.get(id)).data)


@mod_projects.route('', methods=['DELETE'])
@login_required
def delete_users():
    """Delete projects"""
    content = request.get_json()
    pks = content['ids']

    deleted_objects = Project.__table__.delete().where(Project.id.in_(ids))
    db.session.execute(deleted_objects)
    db.session.commit()

    return jsonify({"status":"success"})

@mod_projects.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_project(id):
    """Delete project"""
    Project.query.filter_by(id=id).delete()

    db.session.commit()

    return jsonify({"status":"OK"})