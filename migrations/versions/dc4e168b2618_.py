"""empty message

Revision ID: dc4e168b2618
Revises: d751982c426c
Create Date: 2022-02-11 01:18:11.307162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc4e168b2618'
down_revision = 'd751982c426c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('show_personal', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'show_personal')
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###
