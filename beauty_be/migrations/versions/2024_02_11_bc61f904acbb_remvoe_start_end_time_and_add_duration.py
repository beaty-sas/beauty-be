"""remvoe start/end time and add duration

Revision ID: bc61f904acbb
Revises: 90baf1d5b5a0
Create Date: 2024-02-11 17:44:10.139281

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bc61f904acbb'
down_revision: Union[str, None] = '90baf1d5b5a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'bookings',
        'start_time',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        'bookings',
        'end_time',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.drop_constraint('merchants_sub_key', 'merchants', type_='unique')
    op.create_index(op.f('ix_merchants_sub'), 'merchants', ['sub'], unique=True)
    op.add_column('offers', sa.Column('duration', sa.Integer(), nullable=False))
    op.drop_column('offers', 'end_time')
    op.drop_column('offers', 'start_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offers', sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('offers', sa.Column('end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('offers', 'duration')
    op.drop_index(op.f('ix_merchants_sub'), table_name='merchants')
    op.create_unique_constraint('merchants_sub_key', 'merchants', ['sub'])
    op.alter_column(
        'bookings',
        'end_time',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.alter_column(
        'bookings',
        'start_time',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
