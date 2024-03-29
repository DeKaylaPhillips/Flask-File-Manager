"""empty message

Revision ID: 6bfc22777bf8
Revises: 
Create Date: 2023-08-18 16:16:03.555710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bfc22777bf8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Files', sa.Column('name', sa.String(), nullable=False))
    op.add_column('Files', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('Files', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.drop_constraint('Files_path_key', 'Files', type_='unique')
    op.create_unique_constraint(None, 'Files', ['name'])
    op.drop_column('Files', 'path')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Files', sa.Column('path', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'Files', type_='unique')
    op.create_unique_constraint('Files_path_key', 'Files', ['path'])
    op.drop_column('Files', 'date_modified')
    op.drop_column('Files', 'date_created')
    op.drop_column('Files', 'name')
    # ### end Alembic commands ###
