import pygame
from time import sleep

from pygame.sprite import Sprite


class Pacman(Sprite):
    """Manage the pacman game object."""

    def __init__(self, screen, game_settings, stats, sb, image_list, death_anim_list, sounds):
        """Initialize instance attributes."""
        super(Pacman, self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.stats = stats
        self.sb = sb
        self.image_list = image_list
        self.image = image_list[5]
        self.death_anim_list = death_anim_list
        self.sounds = sounds
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().center
        self.rect.y += 205
        self.center = float(self.rect.centerx)
        self.current_position = None
        self.next_image = 0
        self.animation_switch = 1
        self.current_angle = 180
        self.death_anim_counter = 0
        self.dots_gone = False
        self.power_dots_gone = False
        self.can_move_right = True
        self.moving_right = False
        self.can_move_left = True
        self.moving_left = True
        self.can_move_up = True
        self.moving_up = False
        self.can_move_down = True
        self.moving_down = False
        self.power_up = False
        self.power_up_time = 0
        self.portal_cooldown = 0

    def blitme(self):
        """Draw pacman at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self, maze, display):
        """Update pacman's position."""
        if self.moving_right and self.can_move_right:
            self.rotate_image(want_angle=360)
            self.rect.centerx += self.game_settings.pacman_speed_factor
        elif self.moving_left and self.can_move_left:
            self.rotate_image(want_angle=180)
            self.rect.centerx -= self.game_settings.pacman_speed_factor
        elif self.moving_up and self.can_move_up:
            self.rotate_image(want_angle=90)
            self.rect.centery -= self.game_settings.pacman_speed_factor
        elif self.moving_down and self.can_move_down:
            self.rotate_image(want_angle=270)
            self.rect.centery += self.game_settings.pacman_speed_factor

        self.switch_images()
        if self.power_up_time >= 1000:
            self.power_up = False
            self.power_up_time = 0
            self.sounds.background_music_scared.stop()
            self.sounds.background_music.play(-1)
        if self.power_up:
            self.power_up_time += 1
        if self.portal_cooldown > 0:
            self.portal_cooldown -= 1

        # Check collisions
        self.check_wall_collisions(maze=maze)
        self.check_shield_collisions(maze=maze)
        self.check_dot_collisions(maze=maze)
        self.check_power_dot_collisions(maze=maze)
        self.check_fruit_collisions(maze=maze)
        self.check_portal_collisions(maze=maze)
        self.check_ghost_collisions(maze=maze, display=display)
        self.update_position(maze=maze)

        # Start new round
        if self.dots_gone and self.power_dots_gone:
            maze.build_maze()
            self.reset_pacman()
            self.dots_gone = False
            self.power_dots_gone = False
            self.stats.level += 1
            self.sb.prep_level()

    def check_wall_collisions(self, maze):
        """Check if pacman hits a wall."""
        wall_collisions = pygame.sprite.spritecollide(self, maze.walls, False)
        if wall_collisions:
            if self.moving_right:
                self.can_move_direction(right=False)
                self.rect.right = wall_collisions[0].rect.left
            elif self.moving_left:
                self.can_move_direction(left=False)
                self.rect.left = wall_collisions[0].rect.right
            elif self.moving_up:
                self.can_move_direction(up=False)
                self.rect.top = wall_collisions[0].rect.bottom
            elif self.moving_down:
                self.can_move_direction(down=False)
                self.rect.bottom = wall_collisions[0].rect.top
        else:
            self.can_move_direction()

    def check_shield_collisions(self, maze):
        """Check if pacman hits a shield."""
        shield_collisions = pygame.sprite.spritecollide(self, maze.shields, False)
        if shield_collisions:
            if self.moving_right:
                self.can_move_direction(right=False)
                self.rect.right = shield_collisions[0].rect.left
            elif self.moving_left:
                self.can_move_direction(left=False)
                self.rect.left = shield_collisions[0].rect.right
            elif self.moving_up:
                self.can_move_direction(up=False)
                self.rect.top = shield_collisions[0].rect.bottom
            elif self.moving_down:
                self.can_move_direction(down=False)
                self.rect.bottom = shield_collisions[0].rect.top

    def check_dot_collisions(self, maze):
        """Check if pacman eats a dot."""
        dot_collisions = pygame.sprite.spritecollide(self, maze.dots, True)
        if dot_collisions:
            for _ in dot_collisions:
                self.stats.score += self.game_settings.dot_points
            self.sounds.eat_dot_sound.play()
            self.sb.prep_score()
            self.sb.check_high_score()
            if len(maze.dots) == 0:
                self.dots_gone = True

    def check_power_dot_collisions(self, maze):
        """Check if pacman eats a power dot."""
        power_dot_collisions = pygame.sprite.spritecollide(self, maze.power_dots, True)
        if power_dot_collisions:
            for _ in power_dot_collisions:
                self.stats.score += self.game_settings.power_dot_points
                self.power_up = True
            for ghost in maze.ghosts:
                ghost.scared()
            self.sounds.eat_dot_sound.play()
            self.sounds.background_music.stop()
            self.sounds.background_music_scared.play(-1)
            maze.time_elapsed = 0
            self.sb.prep_score()
            self.sb.check_high_score()
            if len(maze.power_dots) == 0:
                self.power_dots_gone = True

    def check_fruit_collisions(self, maze):
        """Check if pacman eats a fruit."""
        fruit_collisions = pygame.sprite.spritecollide(self, maze.fruits, True)
        if fruit_collisions:
            for _ in fruit_collisions:
                self.stats.score += self.game_settings.fruit_points
            self.sb.prep_score()
            self.sb.check_high_score()

    def check_portal_collisions(self, maze):
        """Check if pacman runs into a portal."""
        portal_collisions = pygame.sprite.spritecollide(self, maze.portals, False)
        if portal_collisions:
            portal = portal_collisions[0]
            if portal.other_portal is not None and self.portal_cooldown == 0:
                self.rect.centerx = portal.other_portal.position.x
                self.rect.centery = portal.other_portal.position.y
                self.portal_cooldown = self.game_settings.portal_cooldown
                self.sounds.portal_transport.play()

    def check_ghost_collisions(self, maze, display):
        """Check if pacman runs into a ghost."""
        ghost_collisions = pygame.sprite.spritecollide(self, maze.ghosts, False)
        # if powered up eat the ghost:
        # else:
        if ghost_collisions:
            if self.power_up:
                for ghost in ghost_collisions:
                    if ghost.worth_points:
                        ghost.dead()
                        self.sounds.ghost_death_sound.play()
                        self.stats.score += self.game_settings.ghost_points
                self.sb.prep_score()
                self.sb.prep_high_score()
            else:
                self.sounds.background_music.stop()
                self.sounds.pacman_death_sound.play()
                maze.ghosts.empty()
                maze.bullets.empty()
                maze.portals.empty()
                self.rotate_image(180)
                for i in range(0, 11):
                    self.death_animation()
                    display.update_screen()
                    sleep(0.1)
                self.reset_pacman()
                self.current_position = None
                self.power_up = False
                if self.stats.lives_left > 0:
                    self.stats.lives_left -= 1
                    self.sb.prep_lives()
                    maze.create_ghosts()
                    self.sounds.background_music.play(-1)
                else:
                    self.sb.save_high_scores()
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)
                pass

    def change_direction(self, right=False, left=False, up=False, down=False):
        """Change the direction and set all other direction to false."""
        self.moving_right, self.moving_left, self.moving_up, self.moving_down = right, left, up, down

    def can_move_direction(self, right=True, left=True, up=True, down=True):
        """Switch which direction is able to be moved in."""
        self.can_move_right, self.can_move_left, self.can_move_up, self.can_move_down = right, left, up, down

    def update_position(self, maze):
        """Update pacman's current node position."""
        node_collisions = pygame.sprite.spritecollide(self, maze.nodes, False)
        if node_collisions:
            self.current_position = node_collisions[0].position

    def switch_images(self):
        """Switch images to animate pacman."""
        self.next_image += self.animation_switch
        if self.next_image == len(self.image_list) or self.next_image == 0:
            self.animation_switch = 0 - self.animation_switch
            self.next_image += self.animation_switch
        self.image = self.image_list[self.next_image]

    def rotate_image(self, want_angle):
        """Rotate the images to match the direction pacman is moving."""
        calc_angle = self.current_angle
        while True:
            calc_angle += 90
            for i in range(0, len(self.image_list)):
                self.image_list[i] = pygame.transform.rotate(self.image_list[i], 90)
            if calc_angle > 360:
                calc_angle = 90
            if calc_angle == want_angle:
                self.current_angle = want_angle
                break

    def reset_pacman(self):
        """Reset pacman after level or death."""
        self.rect.center = self.screen.get_rect().center
        self.rect.y += 205
        self.can_move_direction()
        self.change_direction()
        self.current_position = None

    def death_animation(self):
        """Play animation on death."""
        self.image = self.death_anim_list[self.death_anim_counter]
        self.death_anim_counter += 1
        if self.death_anim_counter >= 11:
            self.death_anim_counter = 0
