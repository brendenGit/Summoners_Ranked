"""empty message

Revision ID: b0778bcebd1d
Revises: a13de8991bb3
Create Date: 2023-11-01 22:37:19.427259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0778bcebd1d'
down_revision = 'a13de8991bb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('summoner_name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('profile_icon_id', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(None, ['puuid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('profile_icon_id')
        batch_op.drop_column('summoner_name')

    # ### end Alembic commands ###