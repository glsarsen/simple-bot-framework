"""empty message

Revision ID: 71a42811374b
Revises: ef87577456a8
Create Date: 2023-01-17 16:24:43.761206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71a42811374b'
down_revision = 'ef87577456a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('email', sa.String(length=120), nullable=True))
    op.add_column('admin', sa.Column('last_seen', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_admin_email'), 'admin', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_column('admin', 'last_seen')
    op.drop_column('admin', 'email')
    # ### end Alembic commands ###