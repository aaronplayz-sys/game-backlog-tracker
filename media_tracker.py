# MediaTracker class — CRUD for media_items, seasons, and episodes

import sqlite3
from models import MediaItem, Season, Episode
from tmdb_client import TMDBClient


class MediaTracker:
    """Handles all CRUD operations for movies, TV shows, seasons, and episodes."""

    def __init__(self, connection, tmdb_client=None):
        self.conn = connection
        self.tmdb = tmdb_client or TMDBClient()

    # =========================================================
    # SEARCH (TMDB passthrough — not a DB write)
    # =========================================================

    def search_tmdb(self, query):
        """Search TMDB for movies/shows to add."""
        return self.tmdb.search(query)

    # =========================================================
    # MEDIA ITEM CRUD
    # =========================================================

    def add_media_item(self, tmdb_id, media_type, title, poster_path=None,
                       overview="", release_date=None):
        """
        CREATE — Add a movie or TV show from TMDB data.
        If it's a TV show, also fetches and creates all seasons + episodes.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO media_items
                    (tmdb_id, media_type, title, poster_path, overview, release_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tmdb_id, media_type, title, poster_path, overview, release_date))
            self.conn.commit()
            media_id = cursor.lastrowid
            print(f"{media_type.title()} '{title}' added successfully.")

            if media_type == "tv":
                self._create_seasons_and_episodes(media_id, tmdb_id)

            return MediaItem(tmdb_id, media_type, title, poster_path,
                             overview, release_date, media_id=media_id)
        except sqlite3.IntegrityError:
            print(f"Error: '{title}' is already in your tracker.")
            return None

    def _create_seasons_and_episodes(self, media_id, tmdb_id):
        """Internal helper — pulls season/episode data from TMDB and stores it."""
        seasons = self.tmdb.get_tv_details(tmdb_id)
        cursor = self.conn.cursor()

        for s in seasons:
            cursor.execute("""
                INSERT INTO seasons (media_id, season_number, episode_count, overview)
                VALUES (?, ?, ?, ?)
            """, (media_id, s["season_number"], s["episode_count"], s["overview"]))
            season_id = cursor.lastrowid

            episodes = self.tmdb.get_season_episodes(tmdb_id, s["season_number"])
            for ep in episodes:
                cursor.execute("""
                    INSERT INTO episodes (season_id, episode_number, title, air_date)
                    VALUES (?, ?, ?, ?)
                """, (season_id, ep["episode_number"], ep["title"], ep["air_date"]))

        self.conn.commit()
        print(f"  Loaded {len(seasons)} season(s) with episodes.")

    def get_all_media(self, media_type=None):
        """READ — Retrieve all media items, optionally filtered by type."""
        cursor = self.conn.cursor()
        if media_type:
            cursor.execute(
                "SELECT * FROM media_items WHERE media_type = ? ORDER BY title",
                (media_type,)
            )
        else:
            cursor.execute("SELECT * FROM media_items ORDER BY title")
        return cursor.fetchall()

    def get_media_by_id(self, media_id):
        """READ — Retrieve a single media item by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM media_items WHERE media_id = ?", (media_id,))
        return cursor.fetchone()

    def update_media_item(self, media_id, status=None, personal_rating=None, notes=None):
        """UPDATE — Update status, rating, or notes for a media item."""
        row = self.get_media_by_id(media_id)
        if not row:
            print(f"No media item found with ID {media_id}.")
            return False
        new_status = status if status is not None else row["status"]
        new_rating = personal_rating if personal_rating is not None else row["personal_rating"]
        new_notes  = notes if notes is not None else row["notes"]
        self.conn.execute("""
            UPDATE media_items
            SET status = ?, personal_rating = ?, notes = ?
            WHERE media_id = ?
        """, (new_status, new_rating, new_notes, media_id))
        self.conn.commit()
        print(f"Media ID {media_id} updated successfully.")
        return True

    def delete_media_item(self, media_id):
        """DELETE — Remove a media item (cascades to seasons/episodes)."""
        row = self.get_media_by_id(media_id)
        if not row:
            print(f"No media item found with ID {media_id}.")
            return False
        self.conn.execute("DELETE FROM media_items WHERE media_id = ?", (media_id,))
        self.conn.commit()
        print(f"'{row['title']}' deleted.")
        return True

    # =========================================================
    # SEASON / EPISODE READ + PROGRESS
    # =========================================================

    def get_seasons_for_media(self, media_id):
        """READ — Get all seasons for a TV show."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM seasons WHERE media_id = ? ORDER BY season_number",
            (media_id,)
        )
        return cursor.fetchall()

    def get_episodes_for_season(self, season_id):
        """READ — Get all episodes for a season."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM episodes WHERE season_id = ? ORDER BY episode_number",
            (season_id,)
        )
        return cursor.fetchall()

    def get_progress(self, media_id):
        """READ — Calculate watched/total episode counts for a TV show."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN e.watched = 1 THEN 1 ELSE 0 END) AS watched
            FROM episodes e
            JOIN seasons s ON e.season_id = s.season_id
            WHERE s.media_id = ?
        """, (media_id,))
        row = cursor.fetchone()
        total = row["total"] or 0
        watched = row["watched"] or 0
        percent = round((watched / total) * 100, 1) if total > 0 else 0
        return {"watched": watched, "total": total, "percent": percent}

    # =========================================================
    # EPISODE UPDATE (mark watched/unwatched)
    # =========================================================

    def toggle_episode_watched(self, episode_id):
        """UPDATE — Toggle an episode's watched status."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT watched FROM episodes WHERE episode_id = ?", (episode_id,))
        row = cursor.fetchone()
        if not row:
            print(f"No episode found with ID {episode_id}.")
            return False
        new_status = 0 if row["watched"] else 1
        watched_date = "DATE('now')" if new_status else "NULL"
        self.conn.execute(f"""
            UPDATE episodes
            SET watched = ?, watched_date = {watched_date}
            WHERE episode_id = ?
        """, (new_status, episode_id))
        self.conn.commit()
        return True
    
    def mark_season_watched(self, season_id, watched=True):
        """UPDATE — Mark all episodes in a season as watched (or unwatched)."""
        new_status = 1 if watched else 0
        watched_date_sql = "DATE('now')" if watched else "NULL"
        self.conn.execute(f"""
            UPDATE episodes
            SET watched = ?, watched_date = {watched_date_sql}
            WHERE season_id = ?
        """, (new_status, season_id))
        self.conn.commit()
        print(f"Season ID {season_id} marked as {'watched' if watched else 'unwatched'}.")
        return True
    
    def get_next_unwatched_episode(self, media_id):
        """Find the next unwatched episode in order across all seasons."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT e.episode_id, e.episode_number, e.title AS episode_title,
                   s.season_number
            FROM episodes e
            JOIN seasons s ON e.season_id = s.season_id
            WHERE s.media_id = ? AND e.watched = 0
            ORDER BY s.season_number, e.episode_number
            LIMIT 1
        """, (media_id,))
        row = cursor.fetchone()
        if row:
            return {
                "episode_id": row["episode_id"],
                "season_number": row["season_number"],
                "episode_number": row["episode_number"],
                "title": row["episode_title"]
            }
        return None  # fully watched