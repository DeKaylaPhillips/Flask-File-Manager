"""empty message

Revision ID: 46ec103a3469
Revises: 542c61d5bdd2
Create Date: 2023-08-21 17:47:36.799721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46ec103a3469'
down_revision = '542c61d5bdd2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('File', sa.Column('headers', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('File', 'headers')
    # ### end Alembic commands ###
