"""empty message

Revision ID: 08c521ee7bb7
Revises: f3e0a4d1876a
Create Date: 2025-02-12 12:16:18.521448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08c521ee7bb7'
down_revision: Union[str, None] = 'f3e0a4d1876a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sellers_info', 'address')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sellers_info', sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
