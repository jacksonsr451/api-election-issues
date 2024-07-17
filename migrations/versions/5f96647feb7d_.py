"""empty message

Revision ID: 5f96647feb7d
Revises: 3c54350e59d5
Create Date: 2024-07-14 11:50:08.605351
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5f96647feb7d'
down_revision: Union[str, None] = '3c54350e59d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'interviewed',
        sa.Column('profession', sa.String(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('marital_status', sa.String(), nullable=False),
        sa.Column('gender', sa.String(), nullable=False),
        sa.Column('education_level', sa.String(), nullable=False),
        sa.Column('neighborhood', sa.String(), nullable=False),
        sa.Column('household_income', sa.String(), nullable=False),
        sa.Column('own_house', sa.String(), nullable=False),
        sa.Column('religion', sa.String(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'questions_answers',
        sa.Column('question_id', sa.UUID(), nullable=False),
        sa.Column('option_id', sa.UUID(), nullable=True),
        sa.Column('response', sa.Text(), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.CheckConstraint(
            '(option_id IS NOT NULL AND response IS NULL) OR (option_id IS NULL AND response IS NOT NULL)',
            name='option_or_response_check',
        ),
        sa.ForeignKeyConstraint(
            ['option_id'],
            ['options.id'],
        ),
        sa.ForeignKeyConstraint(
            ['question_id'],
            ['questions.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'answers',
        sa.Column('device_location', sa.Text(), nullable=True),
        sa.Column('issue_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('interviewed_id', sa.UUID(), nullable=False),
        sa.Column('questions_answers_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ['interviewed_id'],
            ['interviewed.id'],
        ),
        sa.ForeignKeyConstraint(
            ['issue_id'],
            ['election_issues.id'],
        ),
        sa.ForeignKeyConstraint(
            ['questions_answers_id'],
            ['questions_answers.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    op.drop_table('questions_answers')
    op.drop_table('interviewed')
    # ### end Alembic commands ###
