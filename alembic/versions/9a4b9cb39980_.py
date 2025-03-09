"""empty message

Revision ID: 9a4b9cb39980
Revises: ff2200f90a31
Create Date: 2025-02-17 12:29:13.165651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a4b9cb39980'
down_revision: Union[str, None] = 'ff2200f90a31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('r_orders',
    sa.Column('order_id', sa.String(), nullable=False),
    sa.Column('customer_id', sa.String(), nullable=False),
    sa.Column('seller_id', sa.String(), nullable=False),
    sa.Column('return_reason', sa.String(), nullable=False),
    sa.Column('complaint_date', sa.DateTime(), nullable=True),
    sa.Column('seller_address', sa.String(), nullable=False),
    sa.Column('pickup_address', sa.String(), nullable=False),
    sa.Column('refund_amount', sa.Integer(), nullable=False),
    sa.Column('refund_status', sa.String(), nullable=False),
    sa.Column('return_status', sa.String(), nullable=False),
    sa.Column('profit_loss', sa.Integer(), nullable=False),
    sa.Column('feedback', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('order_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('r_orders')
    # ### end Alembic commands ###
