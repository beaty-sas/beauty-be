"""init db

Revision ID: 79a36ff60559
Revises:
Create Date: 2024-02-09 22:48:25.127154

"""
from typing import Sequence
from typing import Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '79a36ff60559'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'attachments',
        sa.Column('original', sa.String(), nullable=False),
        sa.Column('thumbnail', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'locations',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'geom',
            geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'),
            nullable=True,
        ),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'offers',
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'users',
        sa.Column('sub', sa.String(length=200), nullable=True),
        sa.Column('display_name', sa.String(length=200), nullable=False),
        sa.Column('phone_number', sa.String(length=100), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sub'),
    )
    op.create_table(
        'merchants',
        sa.Column('sub', sa.String(length=200), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('phone_number', sa.String(length=100), nullable=True),
        sa.Column('logo_id', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['logo_id'],
            ['attachments.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sub'),
    )
    op.create_table(
        'businesses',
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('display_name', sa.String(length=200), nullable=False),
        sa.Column('phone_number', sa.String(length=100), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('logo_id', sa.Integer(), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['location_id'],
            ['locations.id'],
        ),
        sa.ForeignKeyConstraint(
            ['logo_id'],
            ['attachments.id'],
        ),
        sa.ForeignKeyConstraint(
            ['owner_id'],
            ['merchants.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_businesses_name'), 'businesses', ['name'], unique=True)
    op.create_table(
        'bookings',
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'business_offers',
        sa.Column('business_id', sa.Integer(), nullable=True),
        sa.Column('offer_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id'],
        ),
        sa.ForeignKeyConstraint(
            ['offer_id'],
            ['offers.id'],
        ),
    )
    op.create_table(
        'working_hours',
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('opening_time', sa.Time(), nullable=False),
        sa.Column('closing_time', sa.Time(), nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_working_hours_date'), 'working_hours', ['date'], unique=False)
    op.create_table(
        'booking_offers_association',
        sa.Column('booking_id', sa.Integer(), nullable=False),
        sa.Column('offer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['booking_id'],
            ['bookings.id'],
        ),
        sa.ForeignKeyConstraint(
            ['offer_id'],
            ['offers.id'],
        ),
        sa.PrimaryKeyConstraint('booking_id', 'offer_id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking_offers_association')
    op.drop_index(op.f('ix_working_hours_date'), table_name='working_hours')
    op.drop_table('working_hours')
    op.drop_table('business_offers')
    op.drop_table('bookings')
    op.drop_index(op.f('ix_businesses_name'), table_name='businesses')
    op.drop_table('businesses')
    op.drop_table('merchants')
    op.drop_table('users')
    op.drop_table('offers')
    op.drop_table('locations')
    op.drop_table('attachments')
    # ### end Alembic commands ###