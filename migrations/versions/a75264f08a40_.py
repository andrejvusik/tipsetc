"""empty message

Revision ID: a75264f08a40
Revises: eb0cb92a1ad4
Create Date: 2022-05-30 16:10:12.490161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a75264f08a40'
down_revision = 'eb0cb92a1ad4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=64), nullable=True),
    sa.Column('path', sa.Unicode(length=128), nullable=True),
    sa.Column('type', sa.Unicode(length=3), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('storage')
    # ### end Alembic commands ###
