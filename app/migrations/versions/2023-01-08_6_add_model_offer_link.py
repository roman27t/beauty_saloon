"""6_Add model offer_link

Revision ID: 76d4132f3739
Revises: 3c952e9a3a9a
Create Date: 2023-01-08 08:30:23.958697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76d4132f3739'
down_revision = '3c952e9a3a9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offer_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('service_name_id', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Numeric(precision=3, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['service_name_id'], ['service_name.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('service_name_id', 'employee_id', name='service_offer_unique')
    )
    op.create_index(op.f('ix_offer_link_service_name_id'), 'offer_link', ['service_name_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_offer_link_service_name_id'), table_name='offer_link')
    op.drop_table('offer_link')
    # ### end Alembic commands ###
