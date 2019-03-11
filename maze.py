import pygame
from pygame.sprite import Group

from maze_image import MazeImage
from ghost import Ghost
from point import Point
from node import Node
from a_star import AStar
from bullet import Bullet
from portal import Portal


class Maze:
    """Build and hold all components of the maze."""

    def __init__(self, screen, game_settings, maze_file, sprite_sheet, pacman, sounds):
        """Initialize instance attributes."""
        self.screen = screen
        self.game_settings = game_settings
        self.maze_file = maze_file
        self.sprite_sheet = sprite_sheet
        self.pacman = pacman
        self.sounds = sounds
        self.maze_rows = []
        self.x_offset = 0
        self.y_offset = 60
        self.walls = Group()
        self.dots = Group()
        self.power_dots = Group()
        self.shields = Group()
        self.nodes = Group()
        self.fruits = Group()
        self.portals = Group()
        self.ghosts = Group()
        self.bullets = Group()
        self.a_star = None
        self.time_elapsed = 2000
        self.animate_ghosts = 0
        self.bullet_indicator = 0
        self.create_blue_portal = False
        self.create_red_portal = False
        self.blue_bullet_position = None
        self.red_bullet_position = None
        for row in maze_file:
            self.maze_rows.append(row)
        maze_file.close()

    def build_maze(self):
        """Build the maze according to the maze layout file."""
        self.ghosts.empty()
        self.dots.empty()
        self.power_dots.empty()
        self.shields.empty()
        self.fruits.empty()
        self.walls.empty()
        self.bullets.empty()
        self.portals.empty()
        maze_layout = self.maze_rows
        for row in maze_layout:
            for char in row:
                if char == 'W':
                    wall = MazeImage(screen=self.screen, image=self.sprite_sheet.wall_image)
                    wall.rect.x += self.x_offset
                    wall.rect.y += self.y_offset
                    self.walls.add(wall)
                elif char == '.':
                    dot = MazeImage(screen=self.screen, image=self.sprite_sheet.dot_image)
                    dot.rect.x += self.x_offset
                    dot.rect.y += self.y_offset
                    self.dots.add(dot)
                    point = Point(x=self.x_offset + 7, y=self.y_offset + 7)
                    node = Node(position=point, rect=dot.rect)
                    self.nodes.add(node)

                elif char == ',':
                    dot = MazeImage(screen=self.screen, image=self.sprite_sheet.dot_image)
                    dot.rect.x += self.x_offset
                    dot.rect.y += self.y_offset
                    point = Point(x=self.x_offset + 7, y=self.y_offset + 7)
                    node = Node(position=point, rect=dot.rect)
                    self.nodes.add(node)
                elif char == 'o':
                    power_dot = MazeImage(screen=self.screen, image=self.sprite_sheet.power_dot_image)
                    power_dot.rect.x += self.x_offset
                    power_dot.rect.y += self.y_offset
                    self.power_dots.add(power_dot)
                    point = Point(x=self.x_offset + 7, y=self.y_offset + 7)
                    node = Node(position=point, rect=power_dot.rect)
                    self.nodes.add(node)
                elif char == '-':
                    shield = MazeImage(screen=self.screen, image=self.sprite_sheet.shield_image)
                    shield.rect.x += self.x_offset
                    shield.rect.y += self.y_offset
                    self.shields.add(shield)
                    point = Point(x=self.x_offset + 7, y=self.y_offset + 7)
                    node = Node(position=point, rect=shield.rect)
                    self.nodes.add(node)
                elif char == 'F':
                    fruit = MazeImage(screen=self.screen, image=self.sprite_sheet.fruit_image)
                    fruit.rect.x += self.x_offset
                    fruit.rect.y += self.y_offset - 5
                    fruit_rect = self.sprite_sheet.shield_image.get_rect()
                    self.fruits.add(fruit)
                    point = Point(x=self.x_offset + 7, y=self.y_offset + 7)
                    node = Node(position=point, rect=fruit_rect)
                    self.nodes.add(node)
                self.x_offset += 15
            self.x_offset = 0
            self.y_offset += 15
        self.a_star = AStar()
        self.a_star.create_nodes(nodes=self.nodes.sprites())
        self.create_ghosts()
        self.y_offset = 60

    def create_ghosts(self):
        """Create the ghosts that hunt pacman."""
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.blinky_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=self.nodes.sprites()[189].position, indicator=0, a_star=self.a_star,
                      pacman=self.pacman, nodes=self.nodes)
        self.ghosts.add(ghost)
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.pinky_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=self.nodes.sprites()[242].position, indicator=1, a_star=self.a_star,
                      pacman=self.pacman, nodes=self.nodes)
        self.ghosts.add(ghost)
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.inky_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=self.nodes.sprites()[246].position, indicator=2, a_star=self.a_star,
                      pacman=self.pacman, nodes=self.nodes)
        self.ghosts.add(ghost)
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.clyde_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=self.nodes.sprites()[249].position, indicator=3, a_star=self.a_star,
                      pacman=self.pacman, nodes=self.nodes)
        self.ghosts.add(ghost)

    def blit(self):
        """Draw the maze and its components to the screen."""
        self.walls.draw(self.screen)
        self.dots.draw(self.screen)
        self.power_dots.draw(self.screen)
        self.shields.draw(self.screen)
        self.fruits.draw(self.screen)
        self.portals.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ghosts.draw(self.screen)

    def update_ghosts(self):
        """Update ghost positions, give them new paths, manage timers for animation switching."""
        if self.pacman.power_up:
            if self.time_elapsed >= 600 and self.time_elapsed % 50 == 0:
                for ghost in self.ghosts:
                    ghost.blink()
            if self.time_elapsed % 200 == 0:
                if self.pacman.current_position.x > self.screen.get_rect().centerx:
                    if self.pacman.current_position.y > self.screen.get_rect().centery:
                        goal = self.nodes.sprites()[1].position
                    else:
                        goal = self.nodes.sprites()[488].position
                else:
                    if self.pacman.current_position.y > self.screen.get_rect().centery:
                        goal = self.nodes.sprites()[37].position
                    else:
                        goal = self.nodes.sprites()[529].position
                for ghost in self.ghosts:
                    if not ghost.is_dead:
                        ghost.gen_new_path(scared=True, goal=goal)
        else:
            for ghost in self.ghosts:
                if ghost.is_scared:
                    ghost.restore()
            if self.time_elapsed >= 2000:
                for ghost in self.ghosts.sprites():
                    ghost.gen_new_path(scatter=True)
                self.time_elapsed = 0

        if self.animate_ghosts >= 200:
            for ghost in self.ghosts.sprites():
                ghost.switch_image()
            self.animate_ghosts = 0
        for ghost in self.ghosts.sprites():
            ghost.update()
        self.time_elapsed += 1
        self.animate_ghosts += 1

    def fire_bullet(self):
        """Fire portal gun bullet from pacman."""
        if len(self.bullets) < 2 and self.pacman.current_position is not None:
            if self.bullet_indicator == 0:
                self.sounds.blue_portal.play()
                new_bullet = Bullet(game_settings=self.game_settings, screen=self.screen, bullet_color=(96, 166, 249),
                                    indicator=self.bullet_indicator, pacman=self.pacman)
                self.bullets.add(new_bullet)
                self.bullet_indicator = 1
            else:
                self.sounds.red_portal.play()
                new_bullet = Bullet(game_settings=self.game_settings, screen=self.screen, bullet_color=(254, 163, 89),
                                    indicator=self.bullet_indicator, pacman=self.pacman)
                self.bullets.add(new_bullet)
                self.bullet_indicator = 0

    def update_bullets(self):
        """Update current bullet positions, check for collisions."""
        for bullet in self.bullets:
            bullet.update()
        self.check_bullet_node_collision()
        self.check_bullet_wall_collision()

    def check_bullet_node_collision(self):
        """Check a bullets last node collision and sets that to it's previous position."""
        for bullet in self.bullets.sprites():
            collisions = pygame.sprite.spritecollide(bullet, self.nodes, False)
            if collisions:
                bullet.previous_position = collisions[0]

    def check_bullet_wall_collision(self):
        """Check if a bullet collides with a wall, destroys bullet, creates a portal."""
        for bullet in self.bullets.sprites():
            collisions = pygame.sprite.spritecollide(bullet, self.walls, False)
            if collisions:
                if bullet.indicator == 0:
                    self.create_blue_portal = True
                    self.blue_bullet_position = bullet.previous_position
                else:
                    self.create_red_portal = True
                    self.red_bullet_position = bullet.previous_position
                bullet.kill()

    def update_portals(self):
        """Check if portals need to be closed."""
        portal_position = None
        if self.create_blue_portal:
            for portal in self.portals.sprites():
                if portal.indicator == 0:
                    portal.closing_portal = True
                else:
                    portal_position = portal.position
                    portal.other_portal = self.blue_bullet_position
            new_portal = Portal(screen=self.screen, image_list=self.sprite_sheet.blue_portal,
                                position=self.blue_bullet_position, indicator=0, other_portal=portal_position)
            self.portals.add(new_portal)
            self.create_blue_portal = False
        if self.create_red_portal:
            for portal in self.portals.sprites():
                if portal.indicator == 1:
                    portal.closing_portal = True
                else:
                    portal_position = portal.position
                    portal.other_portal = self.red_bullet_position
            new_portal = Portal(screen=self.screen, image_list=self.sprite_sheet.red_portal,
                                position=self.red_bullet_position, indicator=1, other_portal=portal_position)
            self.portals.add(new_portal)
            self.create_red_portal = False
        self.portals.update()
