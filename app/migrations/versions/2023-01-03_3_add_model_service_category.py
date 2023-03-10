"""3_Add model category

Revision ID: 8ef458757e4c
Revises: 33acdea24464
Create Date: 2023-01-03 12:30:33.218259

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '8ef458757e4c'
down_revision = '33acdea24464'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('detail', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    # ### end Alembic commands ###
