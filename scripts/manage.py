import asyncio
import sys
import os
from alembic.config import Config
from alembic import command

def run_migrations(argv):
    alembic_cfg = Config("alembic.ini")
    
    # Override the SQLite URL if we're in a Docker environment
    if os.getenv("DATABASE_URL"):
        alembic_cfg.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
    
    if len(argv) < 2:
        print("Available commands:")
        print("  migrate - Run all pending migrations")
        print("  revision <message> - Create a new migration")
        print("  downgrade - Downgrade one revision")
        return

    if argv[1] == "migrate":
        command.upgrade(alembic_cfg, "head")
    elif argv[1] == "revision":
        if len(argv) < 3:
            print("Please provide a revision message")
            return
        command.revision(alembic_cfg, argv[2], autogenerate=True)
    elif argv[1] == "downgrade":
        command.downgrade(alembic_cfg, "-1")
    else:
        print(f"Unknown command: {argv[1]}")

if __name__ == "__main__":
    run_migrations(sys.argv) 