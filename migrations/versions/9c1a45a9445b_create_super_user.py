import uuid
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import text

from domain.auth.services.password_encryption_service import (
    PasswordEncryptionService,
)

# revision identifiers, used by Alembic.
revision: str = '9c1a45a9445b'
down_revision: Union[str, None] = '0183cb44252e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_id = str(uuid.uuid4())
    password = PasswordEncryptionService.encrypt_password('admin')

    # Inserir o super usuário
    op.execute(
        f"""
        INSERT INTO users (id, email, password, created_at, updated_at) VALUES 
        ('{user_id}', 'jacksonsr45@gmail.com', '{password}', '{datetime.now()}', '{datetime.now()}');
        """
    )

    # Obter o ID da role 'admin'
    connection = op.get_bind()
    result = connection.execute(
        text("SELECT id FROM roles WHERE name='admin'")
    )
    admin_role_id = result.fetchone()[0]

    # Inserir o relacionamento do usuário com a role 'admin'
    op.execute(
        f"""
        INSERT INTO user_role (user_id, role_id) VALUES 
        ('{user_id}', '{admin_role_id}');
        """
    )


def downgrade() -> None:
    connection = op.get_bind()

    # Obter o ID do super usuário
    result = connection.execute(
        text("SELECT id FROM users WHERE email='jacksonsr45@gmail.com'")
    )
    user_id = result.fetchone()[0]

    # Remover a associação do usuário com a role 'admin'
    op.execute(
        f"""
        DELETE FROM user_role WHERE user_id='{user_id}';
        """
    )

    # Remover o super usuário
    op.execute(
        f"""
        DELETE FROM users WHERE id='{user_id}';
        """
    )
