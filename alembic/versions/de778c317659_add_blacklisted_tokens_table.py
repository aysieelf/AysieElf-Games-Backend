"""add new table

Revision ID: bfdb45635537
Revises: 89db94858bf6
Create Date: 2025-01-22 14:35:10.172065

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "bfdb45635537"
down_revision: Union[str, None] = "89db94858bf6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'blacklisted_tokens',
        sa.Column('token', sa.String, primary_key=True, index=True),
        sa.Column('blacklisted_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('blacklisted_tokens')
