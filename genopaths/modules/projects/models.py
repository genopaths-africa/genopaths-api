from flask_sqlalchemy import SQLAlchemy
from genopaths import db, ma;
import datetime
import enum
from marshmallow_enum import EnumField

class VisibilityEnum(enum.Enum):
    public='public'
    private='private'
    shared='shared'

class CategoryEnum(enum.Enum):
    human='human'
    animals='animals'
    environment='environment'

class Project(db.Model):
    """Project model"""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, db.Sequence('seq_projects_id', ), primary_key=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.Enum(CategoryEnum), nullable=False, default='human')
    visibility = db.Column(db.Enum(VisibilityEnum), nullable=False, default='private')
    created_by = db.Column(db.Integer, nullable=False, default=0)
    updated_by = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self,name, description, category = 'human', visibility = 'private', created_by = 0, updated_by = 0, created_at = None, updated_at = None):
        self.name = name
        self.description = description
        self.category = category
        self.visibility = visibility
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at or datetime.datetime.utcnow()
        self.updated_at = updated_at or datetime.datetime.utcnow()


class ProjectSchema(ma.Schema):
    """Flask Marshmallow Schema for Project model"""
    visibility = EnumField(VisibilityEnum, by_value=True)
    category = EnumField(CategoryEnum, by_value=True)

    class Meta:
        model = Project
        fields = ('id','name','description', 'category', 'visibility', 'created_at','updated_at','created_by','updated_by')

