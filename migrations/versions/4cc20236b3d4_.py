"""empty message

Revision ID: 4cc20236b3d4
Revises: c4bf517fddd4
Create Date: 2019-06-19 21:02:04.013228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cc20236b3d4'
down_revision = 'c4bf517fddd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('assigned_consultants', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'assigned_consultants')
    # ### end Alembic commands ###
