"""Fix product schema

Revision ID: 38dd1e10aeb1
Revises: c23db09d7ed7
Create Date: 2025-02-11 14:48:08.482882

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic.
revision: str = '38dd1e10aeb1'
down_revision: Union[str, None] = 'c23db09d7ed7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add new columns
    op.add_column('products', sa.Column('product_name', sa.String(length=255), nullable=False))
    op.add_column('products', sa.Column('product_description', sa.String(), nullable=True))
    op.add_column('products', sa.Column('stock_quantity', sa.Integer(), nullable=False))
    op.add_column('products', sa.Column('weight', sa.String(length=255), nullable=False))
    op.add_column('products', sa.Column('category_id', sa.String(), nullable=False))  # Fixed typo
    op.add_column('products', sa.Column('brand', sa.String(length=255), nullable=True))
    op.add_column('products', sa.Column('product_image', sa.LargeBinary(), nullable=True))  # Fixed data type
    op.add_column('products', sa.Column('status', sa.String(), nullable=False))
    op.add_column('products', sa.Column('product_tags', sa.String(length=255), nullable=True))
    op.add_column('products', sa.Column('warranty_period', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('return_policy', sa.String(), nullable=True))

    # Modify column types
    op.alter_column('products', 'price',
        existing_type=sa.INTEGER(),
        type_=sa.String(length=10),  # Removed invalid collation
        existing_nullable=False)

    op.alter_column('products', 'created_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=False)

    # Drop incorrect or redundant columns
    op.drop_column('products', 'catgorie_id')  # Fixed typo
    op.drop_column('products', 'Product_detais')  # Fixed typo
    op.drop_column('products', 'product_status')  # Removing based on your previous script
    op.drop_column('products', 'discount')  # Removing based on your previous script
    op.drop_column('products', 'verify')  # Removing based on your previous script
    # op.drop_column('products', 'seller_id')  # Removed this line if you still need 'seller_id'

def downgrade() -> None:
    # Revert the changes
    op.add_column('products', sa.Column('verify', sa.Boolean(), nullable=False, default=False))
    op.add_column('products', sa.Column('discount', sa.String(), nullable=False))
    op.add_column('products', sa.Column('product_status', sa.String(), nullable=False))
    op.add_column('products', sa.Column('Product_detais', sa.String(), nullable=False))
    op.add_column('products', sa.Column('catgorie_id', sa.String(), nullable=False))
    # op.add_column('products', sa.Column('seller_id', sa.String(), nullable=False))  # Restore if needed

    op.alter_column('products', 'created_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=True)

    op.alter_column('products', 'price',
        existing_type=sa.String(length=10),
        type_=sa.INTEGER(),
        existing_nullable=False)

    op.drop_column('products', 'return_policy')
    op.drop_column('products', 'warranty_period')
    op.drop_column('products', 'product_tags')
    op.drop_column('products', 'status')
    op.drop_column('products', 'product_image')
    op.drop_column('products', 'brand')
    op.drop_column('products', 'category_id')
    op.drop_column('products', 'weight')
    op.drop_column('products', 'stock_quantity')
    op.drop_column('products', 'product_description')
    op.drop_column('products', 'product_name')
