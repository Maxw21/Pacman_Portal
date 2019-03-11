import random

from pygame.sprite import Sprite
from point import Point


class Ghost(Sprite):
    """Manages ghosts"""

    def __init__(self, screen, game_settings, image_list, scared_image, blink_image, start_position,
                 indicator, a_star, pacman, nodes):
        """Initialize instance attributes."""
        super(Ghost, self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.image_list = image_list
        self.image = image_list[0]
        self.scared_image = scared_image
        self.blink_image = blink_image
        self.rect = self.image.get_rect()
        self.rect.centerx = start_position.x
        self.rect.centery = start_position.y
        self.previous_position = Point(self.rect.centerx, self.rect.centery)
        self.pacman = pacman
        self.nodes = nodes
        self.indicator = indicator
        self.a_star = a_star
        self.path = None
        self.destination = None
        self.worth_points = False
        self.is_dead = False
        self.is_scared = False
        self.current_image_ind = 0
        self.animation_switch = -1

    def blitme(self):
        """Draw pacman at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update ghost position."""
        if self.destination is not None:
            if self.rect.centerx == self.destination.x and\
                    self.rect.centery == self.destination.y and len(self.path) > 0:
                self.previous_position = self.destination
                self.destination = Point(self.path[0][0], self.path[0][1])
                self.path.pop(0)
            elif len(self.path) == 0:
                self.gen_new_path()
            direction_x = self.destination.x - self.rect.centerx
            direction_y = self.destination.y - self.rect.centery
            if direction_x < 0:
                if not self.is_scared:
                    self.image = self.image_list[self.current_image_ind]
                    if not self.is_dead:
                        self.current_image_ind = 2
                    else:
                        self.current_image_ind = 9
                    self.animation_switch = -1
                self.rect.centerx -= self.game_settings.ghost_speed_factor
            elif direction_x > 0:
                if not self.is_scared:
                    self.image = self.image_list[self.current_image_ind]
                    if not self.is_dead:
                        self.current_image_ind = 4
                    else:
                        self.current_image_ind = 10
                    self.animation_switch = -1
                self.rect.centerx += self.game_settings.ghost_speed_factor
            if direction_y < 0:
                if not self.is_scared:
                    self.image = self.image_list[self.current_image_ind]
                    if not self.is_dead:
                        self.current_image_ind = 0
                    else:
                        self.current_image_ind = 8
                    self.animation_switch = -1
                self.rect.centery -= self.game_settings.ghost_speed_factor
            elif direction_y > 0:
                if not self.is_scared:
                    self.image = self.image_list[self.current_image_ind]
                    if not self.is_dead:
                        self.current_image_ind = 6
                    else:
                        self.current_image_ind = 11
                    self.animation_switch = -1
                self.rect.centery += self.game_settings.ghost_speed_factor
        else:
            self.gen_new_path(scatter=True)

    def gen_new_path(self, scatter=False, scared=False, goal=None, dead=False):
        """Generate a new path for the ghost."""
        if self.pacman.current_position is not None:
            if scatter:
                if self.indicator == 0:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[1].position)
                    self.update_path(path=path)
                elif self.indicator == 1:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[37].position)
                    self.update_path(path=path)
                elif self.indicator == 2:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[488].position)
                    self.update_path(path=path)
                elif self.indicator == 3:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[529].position)
                    self.update_path(path=path)
            elif scared:
                path = self.a_star.get_path(start=self.previous_position, goal=goal)
                self.update_path(path=path)
                pass
            elif dead:
                if self.indicator == 0:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[222].position)
                    self.update_path(path=path)
                elif self.indicator == 1:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[225].position)
                    self.update_path(path=path)
                elif self.indicator == 2:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[266].position)
                    self.update_path(path=path)
                elif self.indicator == 3:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.nodes.sprites()[269].position)
                    self.update_path(path=path)
            else:
                if self.is_dead:
                    self.is_dead = False
                if self.indicator == 0:
                    path = self.a_star.get_path(start=self.previous_position, goal=self.pacman.current_position)
                    self.update_path(path=path)
                elif self.indicator == 1:
                    path = self.a_star.get_path(start=self.previous_position,
                                                goal=self.nodes.sprites()[random.randint(0, 529)].position)
                    self.update_path(path=path)
                elif self.indicator == 2:
                    path = self.a_star.get_path(start=self.previous_position,
                                                goal=self.nodes.sprites()[random.randint(0, 529)].position)
                    self.update_path(path=path)
                elif self.indicator == 3:
                    if abs(self.previous_position.x - self.pacman.current_position.x) > 200 or abs(
                            self.previous_position.y - self.pacman.current_position.y) > 200:
                        path = self.a_star.get_path(start=self.previous_position, goal=self.pacman.current_position)
                        self.update_path(path=path)
                    else:
                        path = self.a_star.get_path(start=self.previous_position,
                                                    goal=self.nodes.sprites()[529].position)
                        self.update_path(path=path)

    def update_path(self, path):
        """Update the path of the ghost."""
        if path is not None:
            self.path = path
            self.destination = Point(path[0][0], path[0][1])
            self.path.pop(0)

    def switch_image(self):
        """Switch between animations."""
        if self.is_scared:
            self.image = self.scared_image
        elif self.is_dead:
            pass
        else:
            self.animation_switch = 0 - self.animation_switch
            self.image = self.image_list[self.current_image_ind + self.animation_switch]
            self.current_image_ind = self.current_image_ind + self.animation_switch

    def scared(self):
        """Change ghost from chasing to running away, change image to blue ghost."""
        self.worth_points = True
        self.is_scared = True

    def blink(self):
        """When power up is ending, start blinking between blue and white."""
        self.image = self.blink_image

    def dead(self):
        """Return to pin after being eaten."""
        self.worth_points = False
        self.gen_new_path(dead=True)
        self.is_dead = True
        self.is_scared = False

    def restore(self):
        """Reset image back to normal after blinking or being eaten."""
        self.image = self.image_list[0]
        self.is_scared = False
