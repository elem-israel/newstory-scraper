"""create tags

Revision ID: 1d3aeda57681
Revises: 9c37a8bfa028
Create Date: 2021-01-23 13:40:11.654342

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "1d3aeda57681"
down_revision = "9c37a8bfa028"
branch_labels = None
depends_on = None


def upgrade():
    with open("sql/2_create_tags.sql") as fp:
        op.execute(fp.read())


def downgrade():
    pass
