"""create data table

Revision ID: 1a847fb2ced0
Revises: aebb445a481f
Create Date: 2023-08-29 00:49:56.104173

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '1a847fb2ced0'
down_revision = 'aebb445a481f'
branch_labels = None
depends_on = None


def upgrade():
    users = op.create_table('data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('data', JSONB, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('now()')),
        sa.Column('created_by', sa.Integer, nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('now()')),
        sa.Column('updated_by', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.execute('ALTER SEQUENCE  data_id_seq RENAME TO seq_data_id')


def downgrade():
    op.drop_table('data')
