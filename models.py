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