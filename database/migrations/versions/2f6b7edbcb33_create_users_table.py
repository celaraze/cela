"""create users table

Revision ID: 2f6b7edbcb33
Revises: 
Create Date: 2023-11-27 15:49:50.262579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2f6b7edbcb33'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(125), nullable=False),
        sa.Column('username', sa.String(125), unique=True),
    )


def downgrade():
    op.drop_table('users')
