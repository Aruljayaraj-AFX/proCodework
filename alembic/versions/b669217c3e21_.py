"""empty message

Revision ID: b669217c3e21
Revises: 51659e1f83f3
Create Date: 2025-02-21 16:27:58.479645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b669217c3e21'
down_revision: Union[str, None] = '51659e1f83f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('inventory_address', sa.String(), nullable=True))
    op.drop_column('inventory_del', 'inventory_address')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory_del', sa.Column('inventory_address', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('inventory', 'inventory_address')
    # ### end Alembic commands ###
