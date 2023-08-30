from flask_sqlalchemy import SQLAlchemy
from genopaths import db, ma;
import datetime
from marshmallow_enum import EnumField
from sqlalchemy.dialects.postgresql import JSONB

class Data(db.Model):
    """Data model"""

    __tablename__ = 'data'

    id = db.Column(db.Integer, db.Sequence('seq_data_id', ), primary_key=True, nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    data = db.Column(JSONB, nullable=True)
    created_by = db.Column(db.Integer, nullable=False, default=0)
    updated_by = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, project_id, data, created_by, updated_by, created_at = None, updated_at = None):
        self.project_id = project_id
        self.data = data
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at or datetime.datetime.utcnow()
        self.updated_at = updated_at or datetime.datetime.utcnow()


class DataSchema(ma.Schema):
    """Flask Marshmallow Schema for Data model"""

    class Meta:
        model = Data
        fields = ('id', 'project_id', 'data', 'created_at','updated_at','created_by','updated_by')