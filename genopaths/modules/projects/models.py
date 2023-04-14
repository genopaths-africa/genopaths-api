from flask_sqlalchemy import SQLAlchemy
from genopaths import db, ma;
import datetime

class Project(db.Model):
    """Project model"""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, db.Sequence('seq_projects_id', ), primary_key=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, nullable=False, default=0)
    updated_by = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self,name, description,created_by, updated_by, created_at, updated_at):
        self.name = name
        self.description = description
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at


class ProjectSchema(ma.Schema):
    """Flask Marshmallow Schema for Project model"""

    class Meta:
        model = Project
        fields = ('id','name','description','created_at','updated_at','created_by','updated_by')