"""empty message

Revision ID: 15634e64736a
Revises: 48a8767504f6
Create Date: 2024-08-04 15:06:45.410170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15634e64736a'
down_revision = '48a8767504f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.String(length=120), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###
