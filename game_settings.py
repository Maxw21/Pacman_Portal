
class GameSettings:
    """Define the settings for the game."""
    def __init__(self):
        # Screen settings
        self.screen_width = 690
        self.screen_height = 865
        self.bg_color = (0, 0, 0)

        # Pacman settings
        self.pacman_speed_factor = 1
        self.lives = 3
        self.portal_cooldown = 500

        # Ghost settings
        self.ghost_speed_factor = 1

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15

        # Score settings
        self.dot_points = 10
        self.power_dot_points = 50
        self.fruit_points = 100
        self.ghost_points = 200
