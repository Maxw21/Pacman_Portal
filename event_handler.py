import sys
import pygame


class EventHandler:
    """Handle all events from user input."""

    def __init__(self, pacman, play_button, score_button, stats, sb, maze, sounds):
        """Initialize instance attributes."""
        self.pacman = pacman
        self.play_button = play_button
        self.score_button = score_button
        self.stats = stats
        self.sb = sb
        self.maze = maze
        self.sounds = sounds
        self.displaying_scores = False

    def check_events(self):
        """Respond to key and mouse presses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sb.save_high_scores()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_key_down_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x=mouse_x, mouse_y=mouse_y)
                self.check_score_button(mouse_x=mouse_x, mouse_y=mouse_y)

    def check_key_down_events(self, event):
        """Respond to key down presses."""
        if event.key == pygame.K_RIGHT:
            self.pacman.change_direction(right=True)
        elif event.key == pygame.K_LEFT:
            self.pacman.change_direction(left=True)
        elif event.key == pygame.K_UP:
            self.pacman.change_direction(up=True)
        elif event.key == pygame.K_DOWN:
            self.pacman.change_direction(down=True)
        elif event.key == pygame.K_SPACE:
            self.maze.fire_bullet()
        elif event.key == pygame.K_q:
            self.sb.save_high_scores()
            sys.exit()

    def check_play_button(self, mouse_x, mouse_y):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            self.sounds.background_music.play(-1)
            self.displaying_scores = False
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_lives()
            self.maze.build_maze()

    def check_score_button(self, mouse_x, mouse_y):
        """Display high scores when the player clicks scores."""
        button_clicked = self.score_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            # Clear the screen, display high scores
            self.displaying_scores = not self.displaying_scores
