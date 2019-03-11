import pygame


class SpriteSheet(object):
    """Load all the sprites from the sprite sheet."""

    def __init__(self, file_name):
        """Initialize instance attributes."""
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.wall_image = self.get_sprite(0, 0, 15, 15)
        self.dot_image = self.get_sprite(0, 15, 15, 15)
        self.power_dot_image = self.get_sprite(15, 0, 15, 15)
        self.shield_image = self.get_sprite(15, 15, 15, 15)
        self.fruit_image = self.get_sprite(30, 0, 30, 30)
        self.ghost_dead_image = self.get_sprite(106, 0, 22, 26)
        self.blink_image = self.get_sprite(60, 0, 22, 26)
        self.blue_portal = []
        self.red_portal = []
        self.pacman_image = []
        self.pacman_death_image = []
        self.blinky_image = []
        self.pinky_image = []
        self.inky_image = []
        self.clyde_image = []
        self.load_all_sprites()
        self.rotate_images()

    def load_all_sprites(self):
        """Append all images to their image list."""
        for i in range(0, 2):
            for j in range(0, 9):
                self.pacman_image.append(self.get_sprite(0 + (34 * j), 30 + (34 * i), 34, 34))
        for i in range(0, 9):
            self.pacman_death_image.append(self.get_sprite(0 + 34 * i, 208, 34, 34))
        for i in range(0, 2):
            self.pacman_death_image.append(self.get_sprite(0 + 34 * i, 242, 34, 34))
        for i in range(0, 12):
            self.inky_image.append(self.get_sprite(0 + 23 * i, 99, 23, 27))
            self.blinky_image.append(self.get_sprite(0 + 23 * i, 126, 23, 27))
            self.pinky_image.append(self.get_sprite(0 + 23 * i, 154, 23, 27))
            self.clyde_image.append(self.get_sprite(0 + 23 * i, 181, 23, 27))
        for i in range(0, 5):
            self.blue_portal.append(self.get_sprite(68 + 34 * i, 242, 34, 34))
            self.red_portal.append(self.get_sprite(68 + 34 * i, 242, 34, 34))
        self.blue_portal.append(self.get_sprite(238, 242, 34, 34))
        self.red_portal.append(self.get_sprite(272, 242, 34, 34))

    def get_sprite(self, x, y, width, height):
        """Split the sprite sheet into individual sprites."""
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return sprite

    def rotate_images(self):
        """Rotate images that need to be rotated."""
        for i in range(0, len(self.pacman_death_image)):
            self.pacman_death_image[i] = pygame.transform.rotate(self.pacman_death_image[i], -90)
