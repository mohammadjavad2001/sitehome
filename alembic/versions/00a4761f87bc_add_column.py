"""add column 

Revision ID: 00a4761f87bc
Revises: 1edc0198eca4
Create Date: 2023-07-05 14:08:17.373661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00a4761f87bc'
down_revision = '1edc0198eca4'
branch_labels = None
depends_on = None


def upgrade() -> None:
            op.add_column('users', sa.Column('profile_picture', sa.String(512)))



def downgrade() -> None:
    pass
