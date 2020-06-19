"""empty message

Revision ID: cc26f080fb7a
Revises: c00d8af94dde
Create Date: 2020-06-16 12:10:15.695715

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cc26f080fb7a'
down_revision = 'c00d8af94dde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('message_id', sa.String(), nullable=True))
    op.alter_column('message', 'message',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('message', 'message',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.drop_column('message', 'message_id')
    # ### end Alembic commands ###
