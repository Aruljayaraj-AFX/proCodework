from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


from models.SELLER.catgories import catgories1
from models.SELLER.discount import discount
from models.SELLER.dummy import otp
from models.SELLER.order import order
from models.SELLER.product_data import product
from models.SELLER.seller import seller
from models.SELLER.seller_info import Seller_info
from models.SELLER.user_data import user_Base
from models.SELLER.subcategories import Base_sub_c
from models.SELLER.return_order import r_order
from models.SELLER.user_address import user_ABase
from models.SELLER.wishlist import wBase 
from models.SELLER.cart import user_cart
from models.payment import payment
from models.inventory import winven
from models.del_data import del_Base
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = catgories1.metadata,discount.metadata,otp.metadata,order.metadata,product.metadata,seller.metadata,Seller_info.metadata,user_Base.metadata,Base_sub_c.metadata,r_order.metadata,user_ABase.metadata,wBase.metadata,user_cart.metadata,payment.metadata,winven.metadata,del_Base.metadata
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
