"""Add documents table

Revision ID: a1b2c3d4e5f6
Revises: 998596108bd5
Create Date: 2026-04-18 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "998596108bd5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("document_name", sa.String(), primary_key=True, index=True),
        sa.Column("storage_path", sa.String(), nullable=False),
        sa.Column("file_type", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.create_index(
        op.f("ix_documents_file_type"), "documents", ["file_type"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_documents_file_type"), table_name="documents")
    op.drop_table("documents")
