"""empty message

Revision ID: fee4e11b1cfc
Revises: bef6934b21f8
Create Date: 2016-03-24 11:25:59.874013

"""

# revision identifiers, used by Alembic.
revision = 'fee4e11b1cfc'
down_revision = 'bef6934b21f8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=120), nullable=False),
    sa.Column('isComplete', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    ### end Alembic commands ###
