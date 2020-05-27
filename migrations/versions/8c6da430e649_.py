"""empty message

Revision ID: 8c6da430e649
Revises: 
Create Date: 2020-05-28 00:52:23.573688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c6da430e649'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=120), nullable=True),
    sa.Column('message', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_user'), 'message', ['user'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_user'), table_name='message')
    op.drop_table('message')
    # ### end Alembic commands ###
