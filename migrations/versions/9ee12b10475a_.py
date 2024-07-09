"""empty message

Revision ID: 9ee12b10475a
Revises: daf775f6bbc7
Create Date: 2024-07-08 18:12:52.418133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ee12b10475a'
down_revision: Union[str, None] = 'daf775f6bbc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('roles_name_key', 'roles', type_='unique')
    op.drop_column('roles', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.create_unique_constraint('roles_name_key', 'roles', ['name'])
    # ### end Alembic commands ###
