"""create projects table

Revision ID: 4d66979c0b70
Revises: 4cfd8359205d
Create Date: 2023-04-14 11:15:08.436855

"""
from alembic import op
import sqlalchemy as sa
import enum


# revision identifiers, used by Alembic.
revision = '4d66979c0b70'
down_revision = '4cfd8359205d'
branch_labels = None
depends_on = None

class VisibilityEnum(enum.Enum):
    public='public'
    private='private'
    shared='shared'

class CategoryEnum(enum.Enum):
    human='human'
    animals='animals'
    environment='environment'

def upgrade():
    users = op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('category', sa.Enum(VisibilityEnum), nullable=False, default='human'),
        sa.Column('visibility', sa.Enum(CategoryEnum), nullable=False, default='private'),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer, nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('now()')),
        sa.Column('updated_by', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('id'),

    )

    op.execute('ALTER SEQUENCE  projects_id_seq RENAME TO seq_projects_id')


def downgrade():
    op.drop_table('projects')
    op.execute("DROP TYPE visibilityenum")
