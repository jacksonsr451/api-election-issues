"""Insert default roles and permissions

Revision ID: ae298944d0dc
Revises: a59eb4bfaa1a
Create Date: 2024-07-08 18:29:47.701362

"""
from datetime import datetime
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = 'ae298944d0dc'
down_revision: Union[str, None] = 'a59eb4bfaa1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Inserir permissões
    read_id = str(uuid.uuid4())
    write_id = str(uuid.uuid4())
    update_id = str(uuid.uuid4())
    delete_id = str(uuid.uuid4())

    op.execute(
        f"""
        INSERT INTO permissions (id, name, created_at, updated_at)
        VALUES 
            ('{read_id}', 'read', '{datetime.now()}', '{datetime.now()}'),
            ('{write_id}', 'write', '{datetime.now()}', '{datetime.now()}'),
            ('{update_id}', 'update', '{datetime.now()}', '{datetime.now()}'),
            ('{delete_id}', 'delete', '{datetime.now()}', '{datetime.now()}')
        """
    )

    # Inserir papéis
    admin_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    editor_id = str(uuid.uuid4())
    guest_id = str(uuid.uuid4())

    # Inserção de dados na tabela 'role'
    op.execute(
        f"""
        INSERT INTO roles (id, name, created_at, updated_at)
        VALUES 
            ('{admin_id}', 'admin', '{datetime.now()}', '{datetime.now()}'),
            ('{user_id}', 'user', '{datetime.now()}', '{datetime.now()}'),
            ('{editor_id}', 'editor', '{datetime.now()}', '{datetime.now()}'),
            ('{guest_id}', 'guest', '{datetime.now()}', '{datetime.now()}')
        """
    )

    op.execute("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """)

    op.create_table(
        'role_permission',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('role_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('permission_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'])
    )

    op.execute(
        f"""
            INSERT INTO role_permission (role_id, permission_id, created_at, updated_at)
            VALUES 
                ('{admin_id}', '{read_id}', '{datetime.now()}', '{datetime.now()}'),
                ('{admin_id}', '{write_id}', '{datetime.now()}', '{datetime.now()}'),
                ('{admin_id}', '{update_id}', '{datetime.now()}', '{datetime.now()}'),
                ('{admin_id}', '{delete_id}', '{datetime.now()}', '{datetime.now()}')
        """
    )

    op.execute(
        f"""
                INSERT INTO role_permission (role_id, permission_id, created_at, updated_at)
                VALUES 
                    ('{user_id}', '{read_id}', '{datetime.now()}', '{datetime.now()}'),
                    ('{user_id}', '{write_id}', '{datetime.now()}', '{datetime.now()}')
            """
    )

    op.execute(
        f"""
                    INSERT INTO role_permission (role_id, permission_id, created_at, updated_at)
                    VALUES 
                        ('{editor_id}', '{read_id}', '{datetime.now()}', '{datetime.now()}'),
                        ('{editor_id}', '{write_id}', '{datetime.now()}', '{datetime.now()}'),
                        ('{editor_id}', '{delete_id}', '{datetime.now()}', '{datetime.now()}')
                """
    )

    op.execute(
        f"""
                INSERT INTO role_permission (role_id, permission_id, created_at, updated_at)
                VALUES 
                    ('{guest_id}', '{read_id}', '{datetime.now()}', '{datetime.now()}')
        """
    )

def downgrade() -> None:
    op.execute("DELETE FROM role_permission WHERE role_id IN (SELECT id FROM role WHERE name IN ('admin', 'user', 'editor', 'guest'))")
    op.execute("DELETE FROM role WHERE name IN ('admin', 'user', 'editor', 'guest')")
    op.execute("DELETE FROM permission WHERE name IN ('read', 'write', 'update', 'delete')")
