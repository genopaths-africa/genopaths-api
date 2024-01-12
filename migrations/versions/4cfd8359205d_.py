"""empty message

Revision ID: 4cfd8359205d
Revises: 
Create Date: 2023-04-14 11:10:59.212453

"""
from alembic import op
import sqlalchemy as sa
import enum

# revision identifiers, used by Alembic.
revision = '4cfd8359205d'
down_revision = None
branch_labels = None
depends_on = None

class RoleEnum(enum.Enum):
    admin = 'admin'
    user = 'user'


def upgrade():
    users = op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=True),
        sa.Column('other_names', sa.String(length=255), nullable=True),
        sa.Column('job_title', sa.String(length=255), nullable=True),
        sa.Column('phone_number', sa.String(length=255), nullable=True),
        sa.Column('photo', sa.Text(), nullable=True),
        sa.Column('token', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum(RoleEnum), nullable=True, default='user'),
        sa.Column('is_account_non_expired', sa.Boolean(), nullable=True, default='yes'),
        sa.Column('is_account_non_locked', sa.Boolean(), nullable=True, default='no'),
        sa.Column('is_enabled', sa.Boolean(), nullable=True, default='yes'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

    op.execute('ALTER SEQUENCE  users_id_seq RENAME TO seq_users_id')
    op.create_unique_constraint('unique_users', 'users', ['username'])
	
    op.bulk_insert(users, [
        {
             'username': 'admin@genopaths.africa',
             'password': 'Password@9',
             'is_enabled': True,
             'token': 'MTYxNjMzMzUyMi41NDc5OTg=',
			 "phone_number":"0753823392",
             "first_name":"admin",
			 "other_names":" ",
			 "role":"admin",
			 "last_name":"admin",
             'job_title': 'Administrator',
			 "is_account_non_expired":False,
			 "is_account_non_locked": False,
			 "photo":"dddd"
         }
    ])


def downgrade():
    op.drop_constraint("unique_users", "users")
    op.drop_table('users')
    op.execute("DROP TYPE roletype")

