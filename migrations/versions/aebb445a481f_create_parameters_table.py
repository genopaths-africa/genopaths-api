"""create parameters table

Revision ID: aebb445a481f
Revises: e36adc79c024
Create Date: 2023-08-21 01:51:37.317420

"""
from alembic import op
import sqlalchemy as sa
import enum

# revision identifiers, used by Alembic.
revision = 'aebb445a481f'
down_revision = 'e36adc79c024'
branch_labels = None
depends_on = None

class OptionalityType(enum.Enum):
    required='required'
    recommended='recommended'
    optional='optional'

def upgrade():
    users = op.create_table('parameters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('ordering', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('type', sa.String(length=255), nullable=True), #number,string,boolean,location,datetime
        sa.Column('validation', sa.String(length=255), nullable=True),
        sa.Column('required', sa.Enum(OptionalityType), nullable=True, default='optional'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer, nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('now()')),
        sa.Column('updated_by', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('id'),

    )

    op.execute('ALTER SEQUENCE  parameters_id_seq RENAME TO seq_parameters_id')


def downgrade():
    op.drop_table('parameters')
    op.execute("DROP TYPE optionalitytype")
