"""empty message

Revision ID: 5f78c0ba7998
Revises: 4cc20236b3d4
Create Date: 2019-06-19 21:16:16.933113

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5f78c0ba7998'
down_revision = '4cc20236b3d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('assigned_consultant', sa.String(length=120), nullable=True))
    op.drop_column('orders', 'assigned_consultants')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('assigned_consultants', mysql.VARCHAR(length=120), nullable=True))
    op.drop_column('orders', 'assigned_consultant')
    # ### end Alembic commands ###
