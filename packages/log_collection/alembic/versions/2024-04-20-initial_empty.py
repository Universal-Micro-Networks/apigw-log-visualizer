"""initial_empty

Revision ID: 3672cf4a76f3
Revises:
Create Date: 2024-04-20 18:13:56.557974

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3672cf4a76f3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 前処理
    pre_upgrade()

    pass

    # 後処理
    post_upgrade()


def downgrade():
    # 前処理
    pre_downgrade()

    pass

    # 後処理
    post_downgrade()


def pre_upgrade():
    # スキーマ更新前に実行する必要がある処理
    pass


def post_upgrade():
    # スキーマ更新後に実行する必要がある処理
    pass


def pre_downgrade():
    # スキーマ更新前に実行する必要がある処理
    pass


def post_downgrade():
    # スキーマ更新後に実行する必要がある処理
    pass
