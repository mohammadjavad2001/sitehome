"""add column 

Revision ID: 1edc0198eca4
Revises: 
Create Date: 2023-07-05 09:35:24.489243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1edc0198eca4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
        op.add_column('users', sa.Column('profile_picture', sa.String(512)))
    


def downgrade() -> None:
    pass
