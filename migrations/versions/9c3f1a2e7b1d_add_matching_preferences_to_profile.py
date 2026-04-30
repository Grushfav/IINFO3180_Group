"""add matching preference fields to profile

Revision ID: 9c3f1a2e7b1d
Revises: 13026aaad071
Create Date: 2026-04-30 01:20:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9c3f1a2e7b1d"
down_revision = "13026aaad071"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("profile", schema=None) as batch_op:
        batch_op.add_column(sa.Column("preferred_min_age", sa.SmallInteger(), nullable=True))
        batch_op.add_column(sa.Column("preferred_max_age", sa.SmallInteger(), nullable=True))
        batch_op.add_column(sa.Column("max_distance_km", sa.SmallInteger(), nullable=True))
        batch_op.add_column(sa.Column("latitude", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("longitude", sa.Float(), nullable=True))

    op.execute("UPDATE profile SET preferred_min_age = 18 WHERE preferred_min_age IS NULL")
    op.execute("UPDATE profile SET preferred_max_age = 60 WHERE preferred_max_age IS NULL")
    op.execute("UPDATE profile SET max_distance_km = 50 WHERE max_distance_km IS NULL")


def downgrade():
    with op.batch_alter_table("profile", schema=None) as batch_op:
        batch_op.drop_column("longitude")
        batch_op.drop_column("latitude")
        batch_op.drop_column("max_distance_km")
        batch_op.drop_column("preferred_max_age")
        batch_op.drop_column("preferred_min_age")
