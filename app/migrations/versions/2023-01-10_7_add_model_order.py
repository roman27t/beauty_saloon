"""7_Add model Order

Revision ID: efa46f5b44ca
Revises: b0b007dadc54
Create Date: 2023-01-10 10:57:02.791557

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'efa46f5b44ca'
down_revision = 'b0b007dadc54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # # hand start
    # status = postgresql.ENUM('WAIT', 'CANCEL', 'PAID', 'SUCCESS', 'PROC_RETURN', 'RETURN', name='status')
    # status.create(op.get_bind())
    # # hand end
    # # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    # sa.Column('status', sa.Enum('WAIT', 'CANCEL', 'PAID', 'SUCCESS', 'PROC_RETURN', 'RETURN', name='status'), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('start_at', sa.DateTime(), nullable=False),
    sa.Column('end_at', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Numeric(precision=7, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expired_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('employee_id', 'start_at', 'end_at', name='order_unique')
    )
    op.create_index(op.f('ix_order_client_id'), 'order', ['client_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_client_id'), table_name='order')
    op.drop_table('order')
    # ### end Alembic commands ###
    # hand start
    # status = postgresql.ENUM('WAIT', 'CANCEL', 'PAID', 'SUCCESS', 'PROC_RETURN', 'RETURN', name='status')
    # status.drop(op.get_bind())
    # hand end
