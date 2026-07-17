class Platform:
    """Represents a gaming platform (e.g., PC, PlayStation 5)."""

    def __init__(self, name, manufacturer, platform_id=None):
        self.platform_id = platform_id
        self.name = name
        self.manufacturer = manufacturer

    def __str__(self):
        return f"[{self.platform_id}] {self.name} by {self.manufacturer}"


class Game:
    """Represents a game title linked to a platform."""

    def __init__(self, title, genre, platform_id, release_year, game_id=None):
        self.game_id = game_id
        self.title = title
        self.genre = genre
        self.platform_id = platform_id
        self.release_year = release_year

    def __str__(self):
        return f"[{self.game_id}] {self.title} ({self.release_year}) - {self.genre}"


class BacklogEntry:
    """Represents a personal tracking entry for a game."""

    VALID_STATUSES = ["Backlog", "Playing", "Completed", "Dropped"]

    def __init__(self, game_id, status, personal_rating=None,
                 hours_played=0.0, notes="", date_added=None, entry_id=None):
        self.entry_id = entry_id
        self.game_id = game_id
        self.status = status
        self.personal_rating = personal_rating  # 1-10, optional
        self.hours_played = hours_played
        self.notes = notes
        self.date_added = date_added

    def __str__(self):
        return (f"[{self.entry_id}] Game ID: {self.game_id} | "
                f"Status: {self.status} | Rating: {self.personal_rating}/10 | "
                f"Hours: {self.hours_played}")

# --- Media Tracking Additions ---

class MediaItem:
    """Represents a movie or TV show, sourced from TMDB."""

    VALID_TYPES = ["movie", "tv"]
    VALID_STATUSES = ["Backlog", "Watching", "Completed", "Dropped"]

    def __init__(self, tmdb_id, media_type, title, poster_path=None,
                 overview="", release_date=None, status="Backlog",
                 personal_rating=None, notes="", media_id=None):
        self.media_id = media_id
        self.tmdb_id = tmdb_id
        self.media_type = media_type
        self.title = title
        self.poster_path = poster_path
        self.overview = overview
        self.release_date = release_date
        self.status = status
        self.personal_rating = personal_rating
        self.notes = notes

    @property
    def poster_url(self):
        """Builds the full TMDB image URL from the stored poster_path."""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None

    def __str__(self):
        return f"[{self.media_id}] {self.title} ({self.media_type}) - {self.status}"


class Season:
    """Represents a season of a TV show."""

    def __init__(self, media_id, season_number, episode_count,
                 overview="", season_id=None):
        self.season_id = season_id
        self.media_id = media_id
        self.season_number = season_number
        self.episode_count = episode_count
        self.overview = overview

    def __str__(self):
        return f"[{self.season_id}] Season {self.season_number} ({self.episode_count} episodes)"


class Episode:
    """Represents a single episode of a TV show season."""

    def __init__(self, season_id, episode_number, title="", air_date=None,
                 watched=False, watched_date=None, episode_id=None):
        self.episode_id = episode_id
        self.season_id = season_id
        self.episode_number = episode_number
        self.title = title
        self.air_date = air_date
        self.watched = watched
        self.watched_date = watched_date

    def __str__(self):
        mark = "✓" if self.watched else "—"
        return f"[{self.episode_id}] E{self.episode_number}: {self.title} {mark}"