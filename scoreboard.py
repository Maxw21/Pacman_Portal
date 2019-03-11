import pygame.font
from pygame.sprite import Group

from pacman import Pacman


class Scoreboard:
    """Report scoring information."""

    def __init__(self, screen, game_settings, stats, sprite_sheet, high_score_file, sounds):
        """Initialize instance attributes."""
        self.screen = screen
        self.game_settings = game_settings
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.sprite_sheet = sprite_sheet
        self.high_score_file = high_score_file
        self.sounds = sounds
        self.high_scores = []
        self.lives = None
        self.score_image = None
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.level_image = None
        self.level_rect = None

        # Font settings
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 32)

        # Prepare initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()
        self.load_high_scores()

    def prep_score(self):
        """Turn the score into a rendered image.."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.game_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.screen_rect.center
        self.score_rect.top = 5

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.game_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 5
        self.score_rect.top = 6

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.game_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.high_score_rect.right
        self.level_rect.top = self.high_score_rect.bottom + 5

    def prep_lives(self):
        """Show how many ships are left."""
        self.lives = Group()
        for life_number in range(self.stats.lives_left):
            life = Pacman(screen=self.screen, game_settings=self.game_settings, stats=self.stats, sb=self,
                          image_list=self.sprite_sheet.pacman_image,
                          death_anim_list=self.sprite_sheet.pacman_death_image, sounds=self.sounds)
            life.rect.x = 10 + life_number * life.rect.width + life_number * 5
            life.rect.bottom = self.screen_rect.bottom - 2
            self.lives.add(life)

    def show_score(self):
        """Draw scores and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)

    def load_high_scores(self):
        """Load the high scores from disk."""
        for line in self.high_score_file:
            self.high_scores.append(int(line))
        self.high_score_file.close()
        if len(self.high_scores) > 0:
            self.stats.high_score = self.high_scores[0]
            self.prep_high_score()

    def save_high_scores(self):
        """Save the high scores before closing and in between games."""
        self.high_scores.append(self.stats.score)
        self.high_scores.sort(reverse=True)
        if len(self.high_scores) > 0:
            self.stats.high_score = self.high_scores[0]
            self.prep_high_score()
        max_score = len(self.high_scores)
        self.high_score_file = open("high_score_file.txt", "w")
        if max_score > 10:
            max_score = 10
        for i in range(0, max_score):
            if self.high_scores[i] > 0:
                self.high_score_file.write(str(int(self.high_scores[i])) + "\n")
        self.high_score_file.close()

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
