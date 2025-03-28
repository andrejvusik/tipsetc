"""empty message

Revision ID: 094ef67ac92e
Revises: 4a1c0d1519ee
Create Date: 2022-02-07 00:23:49.312631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '094ef67ac92e'
down_revision = '4a1c0d1519ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('slug', sa.String(length=128), nullable=True),
    sa.Column('content', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.add_column('users', sa.Column('telegram', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_users_telegram'), 'users', ['telegram'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_telegram'), table_name='users')
    op.drop_column('users', 'telegram')
    op.drop_table('posts')
    # ### end Alembic commands ###
