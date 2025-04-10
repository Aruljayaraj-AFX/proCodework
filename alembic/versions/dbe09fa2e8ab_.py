"""empty message

Revision ID: dbe09fa2e8ab
Revises: 01856cb3f3bf
Create Date: 2025-02-21 15:39:36.233715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbe09fa2e8ab'
down_revision: Union[str, None] = '01856cb3f3bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory_del', sa.Column('delivery_address', sa.String(), nullable=True))
    op.add_column('inventory_del', sa.Column('delivery_city', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory_del', 'delivery_city')
    op.drop_column('inventory_del', 'delivery_address')
    # ### end Alembic commands ###
