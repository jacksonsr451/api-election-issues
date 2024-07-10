import uuid
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0183cb44252e'
down_revision: Union[str, None] = '645e55cd9ba4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Generate UUIDs for permissions and roles
    read_id = str(uuid.uuid4())
    view_id = str(uuid.uuid4())
    update_id = str(uuid.uuid4())
    delete_id = str(uuid.uuid4())

    user_id = str(uuid.uuid4())
    guest_id = str(uuid.uuid4())
    editor_id = str(uuid.uuid4())
    admin_id = str(uuid.uuid4())

    op.execute(
        f"""
            INSERT INTO permissions (id, name, created_at, updated_at) VALUES
            ('{read_id}', 'read', '{datetime.now()}', '{datetime.now()}'),
            ('{view_id}', 'view', '{datetime.now()}', '{datetime.now()}'),
            ('{update_id}', 'update', '{datetime.now()}', '{datetime.now()}'),
            ('{delete_id}', 'delete', '{datetime.now()}', '{datetime.now()}');
            """
    )

    op.execute(
        f"""
            INSERT INTO roles (id, name, created_at, updated_at) VALUES
            ('{user_id}', 'user', '{datetime.now()}', '{datetime.now()}'), 
            ('{guest_id}', 'guest', '{datetime.now()}', '{datetime.now()}'), 
            ('{editor_id}', 'publisher', '{datetime.now()}', '{datetime.now()}'), 
            ('{admin_id}', 'admin', '{datetime.now()}', '{datetime.now()}');
            """
    )

    op.execute(
        f"""
            INSERT INTO role_permission (role_id, permission_id) VALUES
            ('{guest_id}', '{read_id}'),
            ('{user_id}', '{read_id}'),
            ('{user_id}', '{view_id}'),
            ('{editor_id}', '{read_id}'),
            ('{editor_id}', '{view_id}'),
            ('{editor_id}', '{update_id}'),
            ('{admin_id}', '{read_id}'),
            ('{admin_id}', '{view_id}'),
            ('{admin_id}', '{update_id}'),
            ('{admin_id}', '{delete_id}');
            """
    )


def downgrade() -> None:
    # Delete associations and records
    op.execute('DELETE FROM role_permission;')
    op.execute('DELETE FROM roles;')
    op.execute('DELETE FROM permissions;')
