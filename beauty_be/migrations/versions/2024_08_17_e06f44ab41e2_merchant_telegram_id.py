"""merchant_telegram_id

Revision ID: e06f44ab41e2
Revises: dd493556db17
Create Date: 2024-08-17 14:52:38.623574

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e06f44ab41e2'
down_revision: Union[str, None] = 'dd493556db17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('merchants', sa.Column('telegram_id', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('merchants', 'telegram_id')
    # ### end Alembic commands ###