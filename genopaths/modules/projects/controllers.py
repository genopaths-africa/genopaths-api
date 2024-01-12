from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify, make_response
from genopaths.modules.projects.models import Project, ProjectSchema
from genopaths.modules.parameters.models import Parameter, ParameterSchema
from genopaths.modules.data.models import Data, DataSchema
from genopaths.extensions import db
from genopaths import app
import datetime
from flask_login import login_required, login_manager
from datetime import datetime
import base64
from sqlalchemy import or_
from sqlalchemy.dialects import postgresql

mod_projects = Blueprint('projects', __name__, url_prefix='/api/projects')

@mod_projects.route('/', methods=['GET'])
@login_required
def get_projects():
    """Get a list of all the projects"""
    name = request.args.get('name')
    visibility = request.args.get('visibility')
    category = request.args.get('category')
    
    ma_schema = ProjectSchema()
    query = Project.query

    if name: query = query.filter(Project.name.like('%{}%'.format(name)))
    if visibility: query = query.filter(Project.visibility.like('%{}%'.format(visibility)))
    if category: query = query.filter(Project.category.like('%{}%'.format(category)))
    
    return jsonify({
        'status': 'success',
        'data': [ma_schema.dump(v) for v in query.all()] 
    })


@mod_projects.route('/<int:id>', methods=['GET'])
@login_required
def get_project(id):
    """Get project details"""

    ma_schema = ProjectSchema()

    return jsonify({
        'status': 'success',
        'data': ma_schema.dump(Project.query.get(id))
    })

@mod_projects.route('/<int:id>/parameters', methods=['GET'])
@login_required
def get_parameters(id):
    """Get project parameter details"""

    ma_schema = ParameterSchema()
    query = Parameter.query.filter(Parameter.project_id==id).order_by(Parameter.ordering.desc())
    
    return jsonify({
        'status': 'success',
        'data': [ma_schema.dump(v) for v in query.all()] 
    })


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

@mod_projects.route('/<int:id>', methods=['POST','PUT', 'PATCH'])
@login_required
def update_project(id):
    """Update project details"""
    content = request.get_json()
    project = Project.query.filter_by(id=id).first()

    if "name" in content: project.name = content['name']
    if "description" in content: project.description = content['description']
    if "visibility" in content: project.visibility = content['visibility']
    if "category" in content: project.category = content['category']

    db.session.commit()

    return jsonify({"status": "success"})


@mod_projects.route('/', methods=['POST'], strict_slashes=False)
@login_required
def add_project():
    """Add a project"""
    content = request.get_json()

    project = Project(
                name=content['name'],
                description=content['description'],
                visibility=content['visibility'],
                category=content['category'],
                created_by=g.currentuser.id,
                updated_by=g.currentuser.id
            )

    db.session.add(project)
    db.session.commit()

    return jsonify({"status":"success", "message": 'Project added successfully'})


@mod_projects.route('/<int:project_id>/parameters/<int:id>', methods=['GET'])
@login_required
def get_parameter(project_id, id):
    """Get parameter details"""

    ma_schema = ParameterSchema()

    return jsonify({
        'status': 'success',
        'data': ma_schema.dump(Parameter.query.get(id))
    })

@mod_projects.route('/<int:project_id>/parameters', methods=['DELETE'])
@login_required
def delete_parameters(project_id):
    """Delete parameters"""
    content = request.get_json()
    pks = content['ids']

    deleted_objects = Parameter.__table__.delete().where(Parameter.id.in_(ids))
    db.session.execute(deleted_objects)
    db.session.commit()

    return jsonify({"status":"success"})

@mod_projects.route('/<int:project_id>/parameters/<int:id>', methods=['DELETE'])
@login_required
def delete_parameter(project_id, id):
    """Delete parameter"""
    Parameter.query.filter_by(id=id).delete()

    db.session.commit()

    return jsonify({"status":"OK"})

@mod_projects.route('/<int:project_id>/parameters', methods=['POST'])
@login_required
def add_parameter(project_id):
    """Add a parameter"""
    content = request.get_json()

    parameter = Parameter(
                name=content['name'],
                description=content['description'],
                validation=content['validation'],
                required=content['required'],
                project_id=project_id,
                created_by=g.currentuser.id,
                updated_by=g.currentuser.id
            )

    db.session.add(parameter)
    db.session.commit()

    return jsonify({"status":"success", "message": 'Parameter added successfully'})


@mod_projects.route('/<int:project_id>/data', methods=['GET'])
@login_required
def get_data(project_id):
    """Get a list of all the data"""
    name = request.args.get('name')
    
    ma_schema = DataSchema()
    query = Data.query.filter(Data.project_id==project_id)

    return jsonify({
        'status': 'success',
        'data': [ma_schema.dump(v) for v in query.all()] 
    })
