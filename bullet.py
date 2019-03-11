import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, game_settings, screen, bullet_color, indicator, pacman):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen
        self.color = bullet_color
        self.indicator = indicator
        self.speed_factor = 1
        self.moving_right = pacman.moving_right
        self.moving_left = pacman.moving_left
        self.moving_up = pacman.moving_up
        self.moving_down = pacman.moving_down
        self.previous_position = None
        if self.moving_right or self.moving_left:
            self.rect = pygame.Rect(0, 0, game_settings.bullet_height, game_settings.bullet_width)
        else:
            self.rect = pygame.Rect(0, 0, game_settings.bullet_width, game_settings.bullet_height)
        self.rect.centerx = pacman.current_position.x
        self.rect.centery = pacman.current_position.y

    def update(self):
        """Move the bullet on the screen."""
        if self.moving_right:
            self.rect.centerx += 2
        elif self.moving_left:
            self.rect.centerx -= 2
        elif self.moving_up:
            self.rect.centery -= 2
        elif self.moving_down:
            self.rect.centery += 2

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
