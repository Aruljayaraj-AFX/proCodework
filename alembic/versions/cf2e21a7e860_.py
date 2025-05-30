"""empty message

Revision ID: cf2e21a7e860
Revises: 7f3f0f9fbe35
Create Date: 2025-02-21 16:24:00.401085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf2e21a7e860'
down_revision: Union[str, None] = '7f3f0f9fbe35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory_del', sa.Column('inventory_address', sa.String()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory_del', 'inventory_address')
    # ### end Alembic commands ###
