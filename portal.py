from pygame.sprite import Sprite


class Portal(Sprite):
    """Manage the portals in the maze."""

    def __init__(self, screen, image_list, position, indicator, other_portal=None):
        """Initialize instance attributes."""
        super(Portal, self).__init__()

        self.screen = screen
        self.image_list = image_list
        self.image = image_list[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = position.position.x
        self.rect.centery = position.position.y
        self.position = position
        self.next_image = 0
        self.indicator = indicator
        self.opening_portal = True
        self.closing_portal = False
        self.other_portal = other_portal

    def blitme(self):
        """Draw the portal at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the images being switched to."""
        if self.opening_portal:
            self.open_portal()
        if self.closing_portal:
            self.close_portal()

    def open_portal(self):
        """Animate portals to open."""
        if self.next_image < len(self.image_list) - 1:
            self.next_image += 1
        else:
            self.opening_portal = False
        self.image = self.image_list[self.next_image]

    def close_portal(self):
        """Animate portals to close."""
        if self.next_image > 0:
            self.next_image -= 1
        else:
            self.kill()
        self.image = self.image_list[self.next_image]
