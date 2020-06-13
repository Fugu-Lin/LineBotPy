"""empty message

Revision ID: 20d4f3393114
Revises: 98ccaa673ad4
Create Date: 2020-06-10 12:14:17.076812

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import Boolean, Column

revision = '20d4f3393114'
down_revision = '98ccaa673ad4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_manager', sa.Boolean))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', sa.Column('is_manager'))
    # ### end Alembic commands ###
