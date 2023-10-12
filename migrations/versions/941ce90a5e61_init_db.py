"""init DB

Revision ID: 941ce90a5e61
Revises: 
Create Date: 2023-10-12 22:03:11.865509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '941ce90a5e61'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('total_reactions', sa.Integer(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('user_uuid', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_uuid'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post',
    sa.Column('post_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('post_text', sa.Text(), nullable=False),
    sa.Column('user_uuid', sa.String(), nullable=False),
    sa.Column('post_uuid', sa.String(), nullable=False),
    sa.Column('reactions', sa.ARRAY(sa.String()), nullable=True),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.user_uuid'], ),
    sa.PrimaryKeyConstraint('post_id'),
    sa.UniqueConstraint('post_uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###
