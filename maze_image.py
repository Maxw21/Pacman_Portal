from pygame.sprite import Sprite


class MazeImage(Sprite):
    """Represent a single tile image of the maze."""

    def __init__(self, screen, image):
        """Initialize instance attributes."""
        super(MazeImage, self).__init__()
        self.screen = screen
        self.image = image
        self.rect = image.get_rect()

    def blitme(self):
        """Draw the dot on the screen."""
        self.screen.blit(self.image, self.rect)
