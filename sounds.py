import pygame


class Sounds:
    """Manage all sound files."""

    def __init__(self):
        """Load all sounds into variables."""
        self.ghost_death_sound = pygame.mixer.Sound('sounds/ghost_death.wav')
        self.intro_sound = pygame.mixer.Sound('sounds/intro.wav')
        self.pacman_death_sound = pygame.mixer.Sound('sounds/pacman_death.wav')
        self.eat_dot_sound = pygame.mixer.Sound('sounds/eat_sound.wav')
        self.eat_dot_sound.set_volume(0.5)
        self.background_music = pygame.mixer.Sound('sounds/background_music.wav')
        self.background_music_scared = pygame.mixer.Sound('sounds/ghost_scared.wav')
        self.blue_portal = pygame.mixer.Sound('sounds/blue_portal.wav')
        self.red_portal = pygame.mixer.Sound('sounds/red_portal.wav')
        self.portal_transport = pygame.mixer.Sound('sounds/portal_transport.wav')
        self.portal_transport.set_volume(0.5)
