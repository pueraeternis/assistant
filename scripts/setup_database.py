# scripts/setup_database.py

import logging
import sqlite3
from pathlib import Path

# --- Configuration ---
DB_FILE = Path("data/company.db")
DB_DATA_PATH = Path("data")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def setup_database() -> None:
    """
    Creates and populates an SQLite database from scratch.
    If the database file already exists, it will be deleted and recreated.
    """
    # 1. Ensure data directory exists and remove old DB file if present
    DB_DATA_PATH.mkdir(parents=True, exist_ok=True)
    if DB_FILE.exists():
        logging.warning("Database file '%s' already exists. It will be removed and recreated.", DB_FILE)
        DB_FILE.unlink()

    conn = None
    try:
        # 2. Connect to database (file will be created automatically)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        logging.info("Database '%s' created and connection established.", DB_FILE)

        # 3. Create tables
        logging.info("Creating tables 'departments' and 'employees'...")

        cursor.execute(
            """
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
        """
        )

        cursor.execute(
            """
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary INTEGER NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        );
        """
        )

        logging.info("Tables successfully created.")

        # 4. Insert sample data
        logging.info("Inserting sample data into tables...")

        departments_to_insert = [
            (1, "Engineering"),
            (2, "Sales"),
            (3, "HR"),
            (4, "Marketing"),
        ]
        cursor.executemany("INSERT INTO departments (id, name) VALUES (?, ?);", departments_to_insert)

        employees_to_insert = [
            (1, "Alice Johnson", "Senior Developer", 120000, 1),
            (2, "Bob Smith", "Sales Manager", 95000, 2),
            (3, "Charlie Brown", "HR Specialist", 70000, 3),
            (4, "Diana Prince", "Junior Developer", 80000, 1),
            (5, "Eve Adams", "Marketing Lead", 105000, 4),
            (6, "Frank White", "DevOps Engineer", 115000, 1),
            (7, "Grace Hall", "Sales Associate", 65000, 2),
        ]
        cursor.executemany(
            "INSERT INTO employees (id, name, position, salary, department_id) VALUES (?, ?, ?, ?, ?);",
            employees_to_insert,
        )

        # 5. Commit and close
        conn.commit()
        logging.info("Data successfully inserted and committed.")

    except sqlite3.Error as e:
        logging.error("SQLite error occurred: %s", e)
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":
    setup_database()
