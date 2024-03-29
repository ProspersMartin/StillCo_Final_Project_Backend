"""empty message

Revision ID: 7f00749cb4e6
Revises: 5f78c0ba7998
Create Date: 2019-06-20 02:03:48.669109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f00749cb4e6'
down_revision = '5f78c0ba7998'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('selected_services', sa.String(length=5000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'selected_services')
    # ### end Alembic commands ###
