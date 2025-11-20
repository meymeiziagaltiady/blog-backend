"""add test data

Revision ID: b3b3542a21f1
Revises: 2ac38375524c
Create Date: 2025-11-20 04:52:40.064174

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b3b3542a21f1"
down_revision: Union[str, Sequence[str], None] = "2ac38375524c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    # insert test admin
    connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:username, :password, :role)
        """
        ),
        {
            "username": "test_admin",
            "password": "$2b$12$fDjv7ocupHNHrTVe.61jje66WWziq/BbbSsJ9pdXeHFvyeWV3k49.",  # test_admin
            "role": "admin",
        },
    )

    # insert test user1
    result = connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:username, :password, :role)
            RETURNING id
        """
        ),
        {
            "username": "test_user1",
            "password": "$2b$12$vlKRoQt3Tmta2cpxuZcFsu82nEJkSnU03eD2a5eIxhfq0OM6aw1Y.",  # test_user1
            "role": "user",
        },
    )

    # get test user1 id
    user_id = result.fetchone()[0]

    # insert test content 1
    connection.execute(
        sa.text(
            """
            INSERT INTO content (title, body, user_id)
            VALUES (:title, :body, :user_id)
        """
        ),
        {
            "title": "Test Title #1",
            "body": "This is content #1 test.",
            "user_id": user_id,
        },
    )

    # insert test user2
    result = connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:username, :password, :role)
            RETURNING id
        """
        ),
        {
            "username": "test_user2",
            "password": "$2a$12$kA5nnCbXswC4EZ7N4Vj8I.lre7U66a86L3c5QEYSXyNGdVKcJT5C2",  # test_ueser2
            "role": "user",
        },
    )

    # get test user2 id
    user_id = result.fetchone()[0]

    # insert test content 2
    connection.execute(
        sa.text(
            """
            INSERT INTO content (title, body, user_id)
            VALUES (:title, :body, :user_id)
        """
        ),
        {
            "title": "Test Title #2",
            "body": "This is content #2 test.",
            "user_id": user_id,
        },
    )

    # insert test admin for deletion 1
    result = connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:u, :p, :r)
            RETURNING id
        """
        ),
        {
            "u": "test_admin_deletion1",
            "p": "$2a$12$rQFYOqs7bJdhUSX75cOn3uc.ATfTKywN.Eqw8IklUpa2i0S.LdwsO",
            "r": "admin",
        },
    )

    # insert test admin for deletion 2
    result = connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:u, :p, :r)
            RETURNING id
        """
        ),
        {
            "u": "test_admin_deletion2",
            "p": "$2a$12$xX35I9aAK4D7Qz8aIM4zEORnKtcypZk8YS.9tRtFXnOP3ODK6/5Q6",
            "r": "admin",
        },
    )

    # insert test user for deletion 1
    result = connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:u, :p, :r)
            RETURNING id
        """
        ),
        {
            "u": "test_user_deletion1",
            "p": "$2a$12$yTstLhSXB8shkaZlABPRyelon0VMxI9HEbRrHuWSw/HcczAO9Kz5O",
            "r": "user",
        },
    )

    # get test user deletion 1 id
    user_id = result.fetchone()[0]

    # inser test content for deletion 1
    connection.execute(
        sa.text(
            """
            INSERT INTO content (title, body, user_id)
            VALUES (:t, :b, :uid)
        """
        ),
        {
            "t": "Deletion Content #1",
            "b": "This is content #1 deletion test.",
            "uid": user_id,
        },
    )

    # inser test content for deletion 2
    connection.execute(
        sa.text(
            """
            INSERT INTO content (title, body, user_id)
            VALUES (:t, :b, :uid)
        """
        ),
        {
            "t": "Deletion Content #2",
            "b": "This is content #2 deletion test.",
            "uid": user_id,
        },
    )

    # inser test user for deletion 2
    connection.execute(
        sa.text(
            """
            INSERT INTO "user" (username, password, role)
            VALUES (:u, :p, :r)
        """
        ),
        {
            "u": "test_user_deletion2",
            "p": "$2a$12$NcqnyMm3ztA4xiF9jrIT9OoltGpFs7ehB1WNEUMW0g8BvziwZX6i2",
            "r": "user",
        },
    )


def downgrade() -> None:
    # delete example content
    op.execute(
        sa.text(
            """
        DELETE FROM content 
        WHERE user_id IN (
            SELECT id FROM "user" 
            WHERE username LIKE 'test_%'
        )
    """
        )
    )

    # delete example users
    op.execute(
        sa.text(
            """
        DELETE FROM "user" 
        WHERE username LIKE 'test_%'
    """
        )
    )
