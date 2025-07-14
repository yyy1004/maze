import pygame
import config
from player import Player
from game_manager import GameManager


pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDHT, config.SCREEN_EHIGHT))
clock = pygame.time.Clock()

# player = Player()
game_manager = GameManager(screen, 1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("red")
    # pygame.display.flip()

    # player.update()

    game_manager.update()

    # screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
