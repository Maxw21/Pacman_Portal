import pygame
from pygame.sprite import Group

from ghost import Ghost
from pacman import Pacman
from point import Point


class Display:
    """Manage all screen displaying."""

    def __init__(self, screen, game_settings, stats, sb, sprite_sheet, play_button, score_button, maze, pacman,
                 event_handler, sounds):
        """Initialize instance attributes."""
        self.screen = screen
        self.game_settings = game_settings
        self.stats = stats
        self.sb = sb
        self.sprite_sheet = sprite_sheet
        self.play_button = play_button
        self.score_button = score_button
        self.maze = maze
        self.pacman = pacman
        self.event_handler = event_handler
        self.sounds = sounds
        self.start_screen_pacman = None
        self.ghosts = Group()
        self.create_start_images = True
        self.animate_time = 0

    def update_screen(self):
        """Update image on the screen."""
        if self.stats.game_active:
            self.screen.fill(self.game_settings.bg_color)
            self.maze.blit()
            self.pacman.blitme()
            self.sb.show_score()
        else:
            if self.event_handler.displaying_scores:
                self.draw_high_scores()
            else:
                # draw ghosts and animate them
                if self.create_start_images:
                    self.create_start_objects()
                    self.create_start_images = False
                self.draw_start_screen()
            self.draw_title()
            self.play_button.draw_button()
            self.score_button.draw_button()
        pygame.display.flip()

    def draw_title(self):
        """Draw the space invader title"""
        font_color = (255, 255, 0)
        font = pygame.font.SysFont(None, 100)
        logo_img = font.render("PACMAN", True, font_color)
        logo_rect = pygame.Rect(0, 0, 200, 50)
        logo_rect.center = self.screen.get_rect().center
        logo_rect.y -= 300
        logo_rect.x -= 45
        self.screen.blit(logo_img, logo_rect)
        top_logo_img = font.render("PORTAL", True, (197, 242, 196))
        top_logo_rect = pygame.Rect(0, 0, 200, 50)
        top_logo_rect.center = self.screen.get_rect().center
        top_logo_rect.y -= 380
        top_logo_rect.x -= 25
        self.screen.blit(top_logo_img, top_logo_rect)

    def draw_start_screen(self):
        self.screen.fill(self.game_settings.bg_color)
        self.score_button.prep_msg("High Scores")
        self.ghosts.draw(self.screen)
        self.draw_ghost_names()
        if self.animate_time >= 200:
            for ghost in self.ghosts.sprites():
                ghost.switch_image()
            self.animate_time = 0
        self.animate_time += 1

    def draw_high_scores(self):
        """Draw the high scores on the high score page"""
        self.sb.high_scores.sort(reverse=True)
        self.screen.fill(self.game_settings.bg_color)
        self.score_button.prep_msg("Return")
        font_color_white = (230, 230, 230)
        font_color_blue = (0, 0, 255)
        font = pygame.font.SysFont(None, 50)
        title_img = font.render("High Scores", True, font_color_blue)
        title_img_rect = pygame.Rect(0, 0, 200, 50)
        title_img_rect.center = self.screen.get_rect().center
        title_img_rect.y -= 180
        self.screen.blit(title_img, title_img_rect)
        offset = -120
        max_score = len(self.sb.high_scores)
        if max_score > 10:
            max_score = 10
        for i in range(0, max_score):
            score_image = font.render(str(self.sb.high_scores[i]), True, font_color_white)
            score_image_rect = pygame.Rect(0, 0, 200, 50)
            score_image_rect.center = self.screen.get_rect().center
            score_image_rect.y += offset
            score_image_rect.x += 70
            self.screen.blit(score_image, score_image_rect)
            offset += 40

    def draw_ghost_names(self):
        """Render the ghost's names as images."""
        font = pygame.font.SysFont(None, 40)
        blinky_name = font.render("Blinky", True, (255, 0, 0))
        blinky_name_rect = pygame.Rect(0, 0, 200, 50)
        blinky_name_rect.center = self.screen.get_rect().center
        blinky_name_rect.y -= 137
        blinky_name_rect.x += 100
        self.screen.blit(blinky_name, blinky_name_rect)
        pinky_name = font.render("Pinky", True, (242, 166, 166))
        pinky_name_rect = pygame.Rect(0, 0, 200, 50)
        pinky_name_rect.center = self.screen.get_rect().center
        pinky_name_rect.y -= 87
        pinky_name_rect.x += 100
        self.screen.blit(pinky_name, pinky_name_rect)
        inky_name = font.render("Inky", True, (105, 243, 247))
        inky_name_rect = pygame.Rect(0, 0, 200, 50)
        inky_name_rect.center = self.screen.get_rect().center
        inky_name_rect.y -= 37
        inky_name_rect.x += 100
        self.screen.blit(inky_name, inky_name_rect)
        clyde_name = font.render("Clyde", True, (243, 142, 68))
        clyde_name_rect = pygame.Rect(0, 0, 200, 50)
        clyde_name_rect.center = self.screen.get_rect().center
        clyde_name_rect.y += 12
        clyde_name_rect.x += 100
        self.screen.blit(clyde_name, clyde_name_rect)

    def create_start_objects(self):
        """Creae the ghosts and pacman once."""
        self.start_screen_pacman = Pacman(screen=self.screen, game_settings=self.game_settings, stats=self.stats,
                                          sb=self.sb, image_list=self.sprite_sheet.pacman_image,
                                          death_anim_list=self.sprite_sheet.pacman_death_image, sounds=self.sounds)
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.blinky_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=Point(self.screen.get_rect().centerx - 40, self.screen.get_rect().centery - 150),
                      indicator=0, a_star=self.maze.a_star, pacman=self.pacman, nodes=self.maze.nodes)
        self.ghosts.add(ghost)
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.pinky_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=Point(self.screen.get_rect().centerx - 40, self.screen.get_rect().centery - 100),
                      indicator=1, a_star=self.maze.a_star, pacman=self.pacman, nodes=self.maze.nodes)
        self.ghosts.add(ghost)
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.inky_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=Point(self.screen.get_rect().centerx - 40, self.screen.get_rect().centery - 50),
                      indicator=2, a_star=self.maze.a_star, pacman=self.pacman, nodes=self.maze.nodes)
        self.ghosts.add(ghost)
        ghost = Ghost(screen=self.screen, game_settings=self.game_settings, image_list=self.sprite_sheet.clyde_image,
                      scared_image=self.sprite_sheet.ghost_dead_image, blink_image=self.sprite_sheet.blink_image,
                      start_position=Point(self.screen.get_rect().centerx - 40, self.screen.get_rect().centery),
                      indicator=3, a_star=self.maze.a_star, pacman=self.pacman, nodes=self.maze.nodes)
        self.ghosts.add(ghost)
