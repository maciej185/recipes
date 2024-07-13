"""empty message

Revision ID: ac6f80daf4c1
Revises: df7b0c0748b0
Create Date: 2024-07-13 09:01:15.913960

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ac6f80daf4c1"
down_revision: Union[str, None] = "df7b0c0748b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ratings",
        sa.Column("rating_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.recipe_id"], ondelete="CASCADE"),
        sa.UniqueConstraint("author_id", "recipe_id"),
        sa.PrimaryKeyConstraint("rating_id"),
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ratings")
    # ### end Alembic commands ###
