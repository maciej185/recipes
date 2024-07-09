"""empty message

Revision ID: 7ca3e0ca6585
Revises: bf2249d76e56
Create Date: 2024-07-09 08:02:29.709171

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7ca3e0ca6585"
down_revision: Union[str, None] = "bf2249d76e56"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_recipe_association_table",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("recipe_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.recipe_id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
        ),
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass