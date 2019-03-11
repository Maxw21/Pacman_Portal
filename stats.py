
class GameStats:
    """Track statistic fot Pacman Portal."""

    def __init__(self, game_settings):
        """Initialize statistics."""
        self.game_settings = game_settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

        # Prep stats
        self.lives_left = self.game_settings.lives
        self.score = 0
        self.level = 1

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.game_settings.lives
        self.score = 0
        self.level = 1
