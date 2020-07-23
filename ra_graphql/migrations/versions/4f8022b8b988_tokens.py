"""tokens

Revision ID: 4f8022b8b988
Revises: 93e6b002ccec
Create Date: 2020-07-18 09:40:55.650072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4f8022b8b988'
down_revision = '93e6b002ccec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens',
    sa.Column('user_id', postgresql.UUID(), nullable=False),
    sa.Column('token', sa.String(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['_ps_users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    # ### end Alembic commands ###
