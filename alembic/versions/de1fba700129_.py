"""empty message

Revision ID: de1fba700129
Revises: 
Create Date: 2025-02-10 15:48:39.214847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de1fba700129'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catgories_info',
    sa.Column('catgorie_id', sa.Integer(), nullable=False),
    sa.Column('catorgie', sa.String(), nullable=False),
    sa.Column('subcatorgie', sa.String(), nullable=False),
    sa.Column('verify', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('catgorie_id')
    )
    op.create_table('discout',
    sa.Column('discount_name', sa.String(), nullable=False),
    sa.Column('discount_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('discount_type', sa.String(), nullable=False),
    sa.Column('discount', sa.Integer(), nullable=False),
    sa.Column('discount_period', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('discount_id')
    )
    op.create_table('dummy_otp_verify',
    sa.Column('email_id', sa.String(), nullable=False),
    sa.Column('otp', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('email_id')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('payment_type', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('delivery_expected', sa.DateTime(), nullable=False),
    sa.Column('no_of_product', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('catgorie_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('discount', sa.String(), nullable=False),
    sa.Column('offer', sa.String(), nullable=False),
    sa.Column('Product_detais', sa.String(), nullable=False),
    sa.Column('product_status', sa.String(), nullable=False),
    sa.Column('verify', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('seller_work',
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('return_period', sa.DateTime(), nullable=False),
    sa.Column('return_info', sa.String(), nullable=False),
    sa.Column('seller_message', sa.String(), nullable=False),
    sa.Column('user_status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('sellers_info',
    sa.Column('seller_id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('DOB_s', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('verify', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('seller_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('DOB', sa.DateTime(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('verify', sa.String(), nullable=False),
    sa.Column('wishlist', sa.Integer(), nullable=False),
    sa.Column('cart', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('sellers_info')
    op.drop_table('seller_work')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('dummy_otp_verify')
    op.drop_table('discout')
    op.drop_table('catgories_info')
    # ### end Alembic commands ###
