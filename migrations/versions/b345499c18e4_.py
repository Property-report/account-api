"""empty message

Revision ID: b345499c18e4
Revises: 0268c485fe0b
Create Date: 2023-05-31 09:50:49.641844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b345499c18e4'
down_revision = '0268c485fe0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reports', sa.Column('headingvaluefound', sa.String(length=300), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reports', 'headingvaluefound')
    # ### end Alembic commands ###
