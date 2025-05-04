"""create tables.

Revision ID: 8c28383d82be
Revises:
Create Date: 2025-05-04 08:36:02.261630
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8c28383d82be"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "company",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
    )

    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column(
            "company_id", sa.Integer, sa.ForeignKey("company.id"), nullable=False
        ),
    )

    op.create_table(
        "team",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column(
            "company_id", sa.Integer, sa.ForeignKey("company.id"), nullable=False
        ),
        sa.Column("description", sa.String(255), nullable=True),
    )

    op.create_table(
        "resource",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("lifecycle_status", sa.String(50), nullable=False),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("owner", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
        sa.Column(
            "company_id", sa.Integer, sa.ForeignKey("company.id"), nullable=False
        ),
    )

    op.create_table(
        "team_members",
        sa.Column("team_id", sa.Integer, sa.ForeignKey("team.id"), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("team_members")
    op.drop_table("resource")
    op.drop_table("team")
    op.drop_table("user")
    op.drop_table("company")
