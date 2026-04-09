import os
from alembic.config import Config
from alembic import command
from v2_one.utils.logger import logger


def run_migrations():
    """
    Run alembic migrations programmatically.
    """
    # Find alembic.ini relative to this file or from CWD
    # In our project structure, alembic.ini is at the root.
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    ini_path = os.path.join(base_dir, "alembic.ini")

    if not os.path.exists(ini_path):
        # Fallback if structure is different
        ini_path = "alembic.ini"

    logger.info(f"Running migrations from {ini_path}...")
    alembic_cfg = Config(ini_path)
    command.upgrade(alembic_cfg, "head")
