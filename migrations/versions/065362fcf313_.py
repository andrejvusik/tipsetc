"""empty message

Revision ID: 065362fcf313
Revises: dabd0e81e327
Create Date: 2022-04-10 14:02:17.618133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '065362fcf313'
down_revision = 'dabd0e81e327'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'language')
    # ### end Alembic commands ###
