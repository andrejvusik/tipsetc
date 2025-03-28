"""empty message

Revision ID: f28de64b08ff
Revises: 065362fcf313
Create Date: 2022-05-02 14:51:02.704018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f28de64b08ff'
down_revision = '065362fcf313'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('registered', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'registered')
    # ### end Alembic commands ###
