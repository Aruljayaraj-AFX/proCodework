"""empty message

Revision ID: 7f3f0f9fbe35
Revises: dbe09fa2e8ab
Create Date: 2025-02-21 16:20:12.122114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f3f0f9fbe35'
down_revision: Union[str, None] = 'dbe09fa2e8ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory_del', sa.Column('delivery_mode', sa.String(), nullable=True))
    op.add_column('inventory_del', sa.Column('shipping_address', sa.String(), nullable=True))
    op.add_column('inventory_del', sa.Column('shipping_city', sa.String(), nullable=True))
    op.add_column('inventory_del', sa.Column('verify', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory_del', 'verify')
    op.drop_column('inventory_del', 'shipping_city')
    op.drop_column('inventory_del', 'shipping_address')
    op.drop_column('inventory_del', 'delivery_mode')
    # ### end Alembic commands ###
