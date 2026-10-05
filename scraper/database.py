
import sqlite3
import csv
from pathlib import Path
from datetime import datetime


DATABASE_FILE = Path("data/coa_architects.db")
CSV_FILE = Path("data/architect_results.csv")

SOURCE_URL = (
    "https://coa.gov.in/search_architectResult.php"
    "?lang=1&level=1&linkid=&lid=289"
)


def create_database(connection):

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS architects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            architect_id TEXT,
            architect_name TEXT,
            registration_number TEXT UNIQUE,
            registration_year INTEGER,
            disciplinary_action TEXT,
            registration_status TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            phone TEXT,
            email TEXT,
            source_url TEXT,
            search_term TEXT,
            collected_at TEXT,
            processing_status TEXT DEFAULT 'success',
            duplicate_status TEXT DEFAULT 'unique',
            error_message TEXT
        )
    """)

    connection.commit()


def add_missing_columns(connection):

    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(architects)")
    existing_columns = {
        row[1] for row in cursor.fetchall()
    }

    columns_to_add = {
        "architect_id": "TEXT",
        "registration_year": "INTEGER",
        "registration_status": "TEXT",
        "city": "TEXT",
        "state": "TEXT",
        "pincode": "TEXT",
        "phone": "TEXT",
        "source_url": "TEXT",
        "processing_status": "TEXT",
        "duplicate_status": "TEXT",
        "error_message": "TEXT"
    }

    for column_name, column_type in columns_to_add.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"ALTER TABLE architects ADD COLUMN "
                f"{column_name} {column_type}"
            )

    connection.commit()


def get_registration_year(registration_number):

    try:
        parts = registration_number.split("/")

        if len(parts) >= 2:
            return int(parts[1])

    except (ValueError, AttributeError):
        pass

    return None


def load_csv_to_database(connection):

    if not CSV_FILE.exists():
        print(f"ERROR: CSV file not found: {CSV_FILE}")
        return

    cursor = connection.cursor()

    with CSV_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        records_inserted = 0
        records_skipped = 0

        for row in reader:

            registration_number = row["Registration Number"]

            registration_year = get_registration_year(
                registration_number
            )

            cursor.execute("""
                SELECT id
                FROM architects
                WHERE registration_number = ?
            """, (registration_number,))

            existing_record = cursor.fetchone()

            if existing_record:

                records_skipped += 1

                continue

            cursor.execute("""
                INSERT INTO architects (
                    architect_name,
                    registration_number,
                    registration_year,
                    disciplinary_action,
                    address,
                    phone,
                    email,
                    source_url,
                    search_term,
                    collected_at,
                    processing_status,
                    duplicate_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["Architect Name"],
                registration_number,
                registration_year,
                row["Disciplinary Action"],
                row["Address"],
                row["Mobile"],
                row["Email ID"],
                SOURCE_URL,
                "Amol",
                datetime.now().isoformat(timespec="seconds"),
                "success",
                "unique"
            ))

            records_inserted += 1

    connection.commit()

    print(f"Records inserted: {records_inserted}")
    print(f"Duplicate records skipped: {records_skipped}")


def create_indexes(connection):

    cursor = connection.cursor()

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_registration_number
        ON architects(registration_number)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_processing_status
        ON architects(processing_status)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS
        idx_registration_year
        ON architects(registration_year)
    """)

    connection.commit()


def main():

    print("Connecting to database...")

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_FILE)

    create_database(connection)

    add_missing_columns(connection)

    create_indexes(connection)

    print("Database schema ready.")

    load_csv_to_database(connection)

    connection.close()

    print("Database upgrade completed.")


if __name__ == "__main__":
    main()
