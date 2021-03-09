"""create tables

Revision ID: 9c37a8bfa028
Revises:
Create Date: 2020-11-25 11:02:45.635372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9c37a8bfa028"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with open("sql/1_create_tables.sql") as fp:
        op.execute(fp.read())


def downgrade():
    pass
