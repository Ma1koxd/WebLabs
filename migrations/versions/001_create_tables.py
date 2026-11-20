"""Создать таблицы книг и пользователей."""

from alembic import op
import sqlalchemy as sa


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("author", sa.String(100), nullable=False),
        sa.Column("description", sa.String(1000), nullable=False),
        sa.CheckConstraint("length(trim(name)) > 0", name="book_name_not_empty"),
        sa.CheckConstraint("length(trim(author)) > 0", name="book_author_not_empty"),
        sa.CheckConstraint("length(trim(description)) > 0", name="book_description_not_empty"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("books")
