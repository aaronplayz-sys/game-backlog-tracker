# tracker.py
# BacklogTracker class — all CRUD operations for all three tables

import sqlite3
from models import Platform, Game, BacklogEntry


class BacklogTracker:
    """Handles all CRUD operations for the Game Backlog Tracker."""

    def __init__(self, connection):
        self.conn = connection

    # =========================================================
    # PLATFORM CRUD
    # =========================================================

    def add_platform(self, name, manufacturer):
        """CREATE — Insert a new platform into the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO platforms (name, manufacturer) VALUES (?, ?)",
                (name, manufacturer)
            )
            self.conn.commit()
            print(f"Platform '{name}' added successfully.")
            return Platform(name, manufacturer, platform_id=cursor.lastrowid)
        except sqlite3.IntegrityError:
            print(f"Error: Platform '{name}' already exists.")
            return None

    def get_all_platforms(self):
        """READ — Retrieve all platforms."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM platforms ORDER BY name")
        rows = cursor.fetchall()
        platforms = [Platform(r["name"], r["manufacturer"], r["platform_id"]) for r in rows]
        return platforms

    def get_platform_by_id(self, platform_id):
        """READ — Retrieve a single platform by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM platforms WHERE platform_id = ?", (platform_id,))
        r = cursor.fetchone()
        if r:
            return Platform(r["name"], r["manufacturer"], r["platform_id"])
        print(f"No platform found with ID {platform_id}.")
        return None

    def update_platform(self, platform_id, name=None, manufacturer=None):
        """UPDATE — Update a platform's name and/or manufacturer."""
        platform = self.get_platform_by_id(platform_id)
        if not platform:
            return False
        new_name = name if name else platform.name
        new_manufacturer = manufacturer if manufacturer else platform.manufacturer
        self.conn.execute(
            "UPDATE platforms SET name = ?, manufacturer = ? WHERE platform_id = ?",
            (new_name, new_manufacturer, platform_id)
        )
        self.conn.commit()
        print(f"Platform ID {platform_id} updated successfully.")
        return True

    def delete_platform(self, platform_id):
        """DELETE — Remove a platform (cascades to games and entries)."""
        platform = self.get_platform_by_id(platform_id)
        if not platform:
            return False
        self.conn.execute("DELETE FROM platforms WHERE platform_id = ?", (platform_id,))
        self.conn.commit()
        print(f"Platform '{platform.name}' deleted (and all related games/entries).")
        return True

    # =========================================================
    # GAME CRUD
    # =========================================================

    def add_game(self, title, genre, platform_id, release_year):
        """CREATE — Insert a new game into the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO games (title, genre, platform_id, release_year) VALUES (?, ?, ?, ?)",
            (title, genre, platform_id, release_year)
        )
        self.conn.commit()
        print(f"Game '{title}' added successfully.")
        return Game(title, genre, platform_id, release_year, game_id=cursor.lastrowid)

    def get_all_games(self):
        """READ — Retrieve all games with their platform name."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT g.*, p.name AS platform_name
            FROM games g
            JOIN platforms p ON g.platform_id = p.platform_id
            ORDER BY g.title
        """)
        return cursor.fetchall()

    def get_game_by_id(self, game_id):
        """READ — Retrieve a single game by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
        r = cursor.fetchone()
        if r:
            return Game(r["title"], r["genre"], r["platform_id"],
                        r["release_year"], r["game_id"])
        print(f"No game found with ID {game_id}.")
        return None

    def update_game(self, game_id, title=None, genre=None,
                    platform_id=None, release_year=None):
        """UPDATE — Update a game's details."""
        game = self.get_game_by_id(game_id)
        if not game:
            return False
        new_title        = title        if title        else game.title
        new_genre        = genre        if genre        else game.genre
        new_platform_id  = platform_id  if platform_id  else game.platform_id
        new_release_year = release_year if release_year else game.release_year
        self.conn.execute("""
            UPDATE games
            SET title = ?, genre = ?, platform_id = ?, release_year = ?
            WHERE game_id = ?
        """, (new_title, new_genre, new_platform_id, new_release_year, game_id))
        self.conn.commit()
        print(f"Game ID {game_id} updated successfully.")
        return True

    def delete_game(self, game_id):
        """DELETE — Remove a game (cascades to backlog entry)."""
        game = self.get_game_by_id(game_id)
        if not game:
            return False
        self.conn.execute("DELETE FROM games WHERE game_id = ?", (game_id,))
        self.conn.commit()
        print(f"Game '{game.title}' deleted.")
        return True

    # =========================================================
    # BACKLOG ENTRY CRUD
    # =========================================================

    def add_entry(self, game_id, status="Backlog", personal_rating=None,
                  hours_played=0.0, notes=""):
        """CREATE — Add a game to the personal backlog."""
        if status not in BacklogEntry.VALID_STATUSES:
            print(f"Invalid status. Choose from: {BacklogEntry.VALID_STATUSES}")
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO backlog_entries
                    (game_id, status, personal_rating, hours_played, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (game_id, status, personal_rating, hours_played, notes))
            self.conn.commit()
            print(f"Backlog entry added for game ID {game_id}.")
            return BacklogEntry(game_id, status, personal_rating,
                                hours_played, notes, entry_id=cursor.lastrowid)
        except sqlite3.IntegrityError:
            print(f"Error: A backlog entry for game ID {game_id} already exists.")
            return None

    def get_all_entries(self):
        """READ — Retrieve all backlog entries with game and platform info."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT be.*, g.title, g.genre, p.name AS platform_name
            FROM backlog_entries be
            JOIN games g ON be.game_id = g.game_id
            JOIN platforms p ON g.platform_id = p.platform_id
            ORDER BY be.status, g.title
        """)
        return cursor.fetchall()

    def get_entry_by_id(self, entry_id):
        """READ — Retrieve a single backlog entry by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM backlog_entries WHERE entry_id = ?", (entry_id,))
        r = cursor.fetchone()
        if r:
            return BacklogEntry(r["game_id"], r["status"], r["personal_rating"],
                                r["hours_played"], r["notes"], r["date_added"],
                                r["entry_id"])
        print(f"No entry found with ID {entry_id}.")
        return None

    def update_entry(self, entry_id, status=None, personal_rating=None,
                     hours_played=None, notes=None):
        """UPDATE — Update a backlog entry's status, rating, hours, or notes."""
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            return False
        if status and status not in BacklogEntry.VALID_STATUSES:
            print(f"Invalid status. Choose from: {BacklogEntry.VALID_STATUSES}")
            return False
        new_status  = status         if status         is not None else entry.status
        new_rating  = personal_rating if personal_rating is not None else entry.personal_rating
        new_hours   = hours_played   if hours_played   is not None else entry.hours_played
        new_notes   = notes          if notes          is not None else entry.notes
        self.conn.execute("""
            UPDATE backlog_entries
            SET status = ?, personal_rating = ?, hours_played = ?, notes = ?
            WHERE entry_id = ?
        """, (new_status, new_rating, new_hours, new_notes, entry_id))
        self.conn.commit()
        print(f"Entry ID {entry_id} updated successfully.")
        return True

    def delete_entry(self, entry_id):
        """DELETE — Remove a backlog entry."""
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            return False
        self.conn.execute(
            "DELETE FROM backlog_entries WHERE entry_id = ?", (entry_id,)
        )
        self.conn.commit()
        print(f"Backlog entry ID {entry_id} deleted.")
        return True