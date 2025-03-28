"""empty message

Revision ID: 636cfd06d470
Revises: d749525c3aa5
Create Date: 2025-02-12 13:01:23.540055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '636cfd06d470'
down_revision: Union[str, None] = 'd749525c3aa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('customer_id', sa.Integer(), nullable=False))
    op.add_column('orders', sa.Column('order_date', sa.DateTime(), nullable=False))
    op.add_column('orders', sa.Column('total_amount', sa.Integer(), nullable=False))
    op.add_column('orders', sa.Column('order_quantity', sa.Integer(), nullable=False))
    op.add_column('orders', sa.Column('payment_status', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('payment_method', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('shipping_address', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('billing_address', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('order_status', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('delivery_date', sa.DateTime(), nullable=True))
    op.add_column('orders', sa.Column('notes', sa.String(), nullable=True))
    op.drop_column('orders', 'user_id')
    op.drop_column('orders', 'payment_type')
    op.drop_column('orders', 'address')
    op.drop_column('orders', 'delivery_expected')
    op.drop_column('orders', 'phone_number')
    op.drop_column('orders', 'no_of_product')
    op.drop_column('orders', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('no_of_product', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('phone_number', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('delivery_expected', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('payment_type', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('user_id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('orders', 'notes')
    op.drop_column('orders', 'delivery_date')
    op.drop_column('orders', 'order_status')
    op.drop_column('orders', 'billing_address')
    op.drop_column('orders', 'shipping_address')
    op.drop_column('orders', 'payment_method')
    op.drop_column('orders', 'payment_status')
    op.drop_column('orders', 'order_quantity')
    op.drop_column('orders', 'total_amount')
    op.drop_column('orders', 'order_date')
    op.drop_column('orders', 'customer_id')
    # ### end Alembic commands ###
