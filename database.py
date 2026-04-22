import sqlite3
import os

DB_NAME = "backlog.db"

class DatabaseManager:
    """Manages the SQLite database connection and schema setup."""

    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """Open a connection to the SQLite database."""
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row  # lets us access columns by name
        self.connection.execute("PRAGMA foreign_keys = ON")  # enforce FK constraints
        print(f"Connected to database: {self.db_name}")

    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def create_tables(self):
        """Create all tables if they don't already exist."""
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS platforms (
                platform_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL UNIQUE,
                manufacturer  TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                title         TEXT NOT NULL,
                genre         TEXT NOT NULL,
                platform_id   INTEGER NOT NULL,
                release_year  INTEGER,
                FOREIGN KEY (platform_id) REFERENCES platforms(platform_id)
                    ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backlog_entries (
                entry_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id         INTEGER NOT NULL UNIQUE,
                status          TEXT NOT NULL DEFAULT 'Backlog',
                personal_rating INTEGER CHECK(personal_rating BETWEEN 1 AND 10),
                hours_played    REAL DEFAULT 0.0,
                notes           TEXT DEFAULT '',
                date_added      TEXT DEFAULT (DATE('now')),
                FOREIGN KEY (game_id) REFERENCES games(game_id)
                    ON DELETE CASCADE
            )
        """)

        self.connection.commit()
        print("Tables created successfully.")

    def get_connection(self):
        """Return the active connection (for use in other modules)."""
        return self.connection