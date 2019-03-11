import pygame

from game_settings import GameSettings
from stats import GameStats
from pacman import Pacman
from sounds import Sounds
from scoreboard import Scoreboard
from maze import Maze
from sprite_sheet import SpriteSheet
from button import Button
from event_handler import EventHandler
from display import Display


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    game_settings = GameSettings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Pac Man Portal")

    # Open sprite sheet
    sprite_sheet = SpriteSheet(file_name='images/spritesheet.png')

    # Make the Play and Scores button.
    play_button = Button(screen=screen, msg="Play", order=0)
    score_button = Button(screen=screen, msg="High Scores", order=1)

    # Open high score file
    try:
        high_score_file = open("high_score_file.txt", "r+")
    except FileNotFoundError:
        high_score_file = open("high_score_file.txt", "w+")

    # Open maze layout file
    maze_file = open('mazelayout.txt', 'r')

    # Make sound manager
    sounds = Sounds()

    # Initialize game stats and scoreboard
    stats = GameStats(game_settings=game_settings)
    sb = Scoreboard(screen=screen, game_settings=game_settings, stats=stats, sprite_sheet=sprite_sheet,
                    high_score_file=high_score_file, sounds=sounds)

    # Initialize pacman
    pacman = Pacman(screen=screen, game_settings=game_settings, stats=stats, sb=sb,
                    image_list=sprite_sheet.pacman_image, death_anim_list=sprite_sheet.pacman_death_image,
                    sounds=sounds)

    # Initialize maze
    maze = Maze(screen=screen, game_settings=game_settings, maze_file=maze_file, sprite_sheet=sprite_sheet,
                pacman=pacman, sounds=sounds)

    # Initialize the event handler
    event_handler = EventHandler(pacman=pacman, play_button=play_button, score_button=score_button, stats=stats, sb=sb,
                                 maze=maze, sounds=sounds)

    # Initialize the display manager
    display = Display(screen=screen, game_settings=game_settings, stats=stats, sb=sb, sprite_sheet=sprite_sheet,
                      play_button=play_button, score_button=score_button, maze=maze, pacman=pacman,
                      event_handler=event_handler, sounds=sounds)

    # Start the main loop for the game
    while True:
        event_handler.check_events()
        if stats.game_active:
            pacman.update(maze=maze, display=display)
            maze.update_ghosts()
            maze.update_bullets()
            maze.update_portals()
        display.update_screen()


run_game()
