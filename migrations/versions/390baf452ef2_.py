"""empty message

Revision ID: 390baf452ef2
Revises: 
Create Date: 2022-09-01 13:22:35.690360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '390baf452ef2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', sa.Column('user_role', sa.VARCHAR(length=1), nullable=True))
    # ### end Alembic commands ###
