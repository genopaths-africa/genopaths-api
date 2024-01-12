from flask_sqlalchemy import SQLAlchemy
from genopaths import db, ma;
import datetime
from marshmallow_enum import EnumField

class Parameter(db.Model):
    """Parameter model"""

    __tablename__ = 'parameters'

    id = db.Column(db.Integer, db.Sequence('seq_parameters_id', ), primary_key=True, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    ordering = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    label = db.Column(db.String(255), unique=True, nullable=False)
    validation = db.Column(db.String(255), nullable=False)
    required = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, nullable=False, default=0)
    updated_by = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, project_id, name, label, description, validation, required, created_by, updated_by, ordering=None, created_at = None, updated_at = None):
        self.name = name
        self.label = label
        self.project_id = project_id
        self.description = description
        self.validation = validation
        self.required = required
        self.ordering = ordering
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at or datetime.datetime.utcnow()
        self.updated_at = updated_at or datetime.datetime.utcnow()


class ParameterSchema(ma.Schema):
    """Flask Marshmallow Schema for Parameter model"""

    class Meta:
        model = Parameter
        fields = ('id', 'project_id', 'name', 'label', 'description', 'validation', 'required', 'ordering', 'created_at','updated_at','created_by','updated_by')