"""add example data

Revision ID: 2ac38375524c
Revises: eb1454d25fcf
Create Date: 2025-11-19 18:36:52.341385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2ac38375524c'
down_revision: Union[str, Sequence[str], None] = 'eb1454d25fcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    connection = op.get_bind()

    # insert example admin
    connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:username, :password, :role)
        """
        ),
        {"username": "admin", "password": "$2b$12$3IG3BFzkZmbQccXEn/o/MeTex.riDirev67JS3.4iduRQW4NllacO", "role": "admin"},
    )

    # insert example user
    result = connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:username, :password, :role)
            RETURNING id
        """
        ),
        {"username": "user", "password": "$2b$12$VjSJwWYRrb6dIIMVwCEUJ.nQQkfvaVRdkHwD.xqhWQfknS/LAu1Ii", "role": "user"},
    )

    # get example user id
    user_id = result.fetchone()[0]

    # insert example content
    connection.execute(
        sa.text(
            """
            INSERT INTO content (title, body, user_id)
            VALUES (:title, :body, :user_id)
        """
        ),
        {
            "title": "Example Title",
            "body": "This is a content example.",
            "user_id": user_id,
        },
    )


def downgrade():
    # delete example content
    op.execute(
        sa.text(
            """
        DELETE FROM content 
        WHERE user_id IN (
            SELECT id FROM "user" 
            WHERE username IN ('admin', 'user')
        )
    """
        )
    )

    # delete example users
    op.execute(
        sa.text(
            """
        DELETE FROM "user" 
        WHERE username IN ('admin', 'user')
    """
        )
    )
