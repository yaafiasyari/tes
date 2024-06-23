"""Initial migration

Revision ID: 7dc792c1fa5d
Revises: 
Create Date: 2024-06-23 05:53:27.376734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7dc792c1fa5d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('user_activity2')
    op.drop_table('landing_product')
    op.drop_table('user_activity')
    op.drop_table('warehouse')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('warehouse',
    sa.Column('itemid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('category', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('date', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sold', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('stock', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('priority', sa.VARCHAR(length=50), autoincrement=False, nullable=True)
    )
    op.create_table('user_activity',
    sa.Column('ProductID', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('StoreID', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('ReportDate', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('SalesCumulativeSum', sa.BIGINT(), autoincrement=False, nullable=True)
    )
    op.create_table('landing_product',
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('category', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('original_price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('discounted_price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('discount_percentage', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('platform', sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.create_table('user_activity2',
    sa.Column('ProductID', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('StoreID', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('ReportDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('SalesCumulativeSum', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    )
    op.drop_table('user')
    op.drop_table('product')
    # ### end Alembic commands ###
