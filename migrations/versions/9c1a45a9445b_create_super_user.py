"""create super user

Revision ID: 9c1a45a9445b
Revises: 0183cb44252e
Create Date: 2024-07-09 19:03:09.132049

"""
from datetime import datetime
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

from domain.auth.services.password_encryption_service import PasswordEncryptionService


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
    result = connection.execute(text("SELECT id FROM roles WHERE name='admin'"))
    admin_role_id = result.fetchone()[0]

    # Inserir o relacionamento do usuário com a role 'admin'
    op.execute(
        f"""
        INSERT INTO user_role (user_id, role_id) VALUES 
        ('{user_id}', '{admin_role_id}');
        """
    )


def downgrade() -> None:
    # Obter o ID do super usuário
    connection = op.get_bind()
    result = connection.execute("SELECT id FROM `user` WHERE email='jacksonsr45@gmail.com'")
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
        DELETE FROM `user` WHERE id='{user_id}';
        """
    )
