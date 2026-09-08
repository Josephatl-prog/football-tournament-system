import os
import sqlite3
from sqlalchemy import create_engine, MetaData, text


# ============================================================
# LOCAL SQLITE DATABASE
# ============================================================

SQLITE_PATH = os.path.join(
    os.path.dirname(__file__),
    "instance",
    "database.db"
)

if not os.path.exists(SQLITE_PATH):
    raise FileNotFoundError(
        f"Could not find local database at: {SQLITE_PATH}"
    )


# ============================================================
# GET POSTGRES DATABASE URL
# ============================================================

POSTGRES_URL = input(
    "Paste your Render Internal Database URL: "
).strip()

if not POSTGRES_URL:
    raise ValueError("PostgreSQL URL cannot be empty.")


# ============================================================
# CONNECT TO BOTH DATABASES
# ============================================================

sqlite_engine = create_engine(
    f"sqlite:///{SQLITE_PATH}"
)

postgres_engine = create_engine(
    POSTGRES_URL
)


# ============================================================
# READ SQLITE TABLES
# ============================================================

sqlite_metadata = MetaData()

sqlite_metadata.reflect(
    bind=sqlite_engine
)

print("\nSQLite tables found:")

for table in sqlite_metadata.sorted_tables:
    print(" -", table.name)


# ============================================================
# COPY DATA
# ============================================================

with sqlite_engine.connect() as source:

    with postgres_engine.begin() as destination:

        # Disable foreign-key checks temporarily
        destination.execute(
            text("SET session_replication_role = 'replica';")
        )

        for table in sqlite_metadata.sorted_tables:

            table_name = table.name

            print(
                f"\nMigrating table: {table_name}"
            )

            rows = source.execute(
                table.select()
            ).mappings().all()

            if not rows:
                print("  No records.")
                continue

            # Get PostgreSQL columns
            postgres_metadata = MetaData()

            postgres_metadata.reflect(
                bind=postgres_engine,
                only=[table_name]
            )

            target_table = postgres_metadata.tables[
                table_name
            ]

            # Clear existing records
            destination.execute(
                target_table.delete()
            )

            # Insert records
            destination.execute(
                target_table.insert(),
                [dict(row) for row in rows]
            )

            print(
                f"  Copied {len(rows)} records."
            )

        # Re-enable foreign-key checks
        destination.execute(
            text("SET session_replication_role = 'origin';")
        )


print("\n========================================")
print("DATABASE MIGRATION COMPLETE")
print("========================================")
