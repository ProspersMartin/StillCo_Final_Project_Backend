"""empty message

Revision ID: aedec32093e5
Revises: 41374fd812f5
Create Date: 2019-06-27 01:12:19.498045

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aedec32093e5'
down_revision = '41374fd812f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_catalog', sa.Column('service_name', sa.String(length=120), nullable=True))
    op.drop_column('service_catalog', 'service')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_catalog', sa.Column('service', mysql.VARCHAR(length=120), nullable=True))
    op.drop_column('service_catalog', 'service_name')
    # ### end Alembic commands ###