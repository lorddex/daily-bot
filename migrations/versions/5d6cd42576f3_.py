"""empty message

Revision ID: 5d6cd42576f3
Revises: cc26f080fb7a
Create Date: 2020-06-19 17:23:37.766109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d6cd42576f3'
down_revision = 'cc26f080fb7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('channel', sa.String(), nullable=True))
    op.add_column('message', sa.Column('event_ts', sa.String(), nullable=True))
    op.add_column('message', sa.Column('ts', sa.String(), nullable=True))
    op.drop_column('message', 'message_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('message_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('message', 'ts')
    op.drop_column('message', 'event_ts')
    op.drop_column('message', 'channel')
    # ### end Alembic commands ###