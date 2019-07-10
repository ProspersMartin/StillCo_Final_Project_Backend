"""empty message

Revision ID: ab16261dd3d2
Revises: aedec32093e5
Create Date: 2019-06-27 02:12:49.766118

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ab16261dd3d2'
down_revision = 'aedec32093e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'payment_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('payment_type', mysql.VARCHAR(length=120), nullable=True))
    # ### end Alembic commands ###