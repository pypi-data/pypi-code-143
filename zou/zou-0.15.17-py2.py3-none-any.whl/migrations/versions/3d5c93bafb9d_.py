"""empty message

Revision ID: 3d5c93bafb9d
Revises: 7dc79d4ed7cd
Create Date: 2018-05-30 20:04:38.461178

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "3d5c93bafb9d"
down_revision = "7dc79d4ed7cd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "project", sa.Column("has_avatar", sa.Boolean(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "has_avatar")
    # ### end Alembic commands ###
