import pygame
from wall import Wall
from player import Player


class GameManager:
    def __init__(self, screen, level=1):
        self.screen = screen
        self.level = level

        self.player = None
        self.walls = pygame.sprite.Group()

        self.load()

    def load_walls(self, walls):
        self.walls.empty()
        for x, y, width, height in walls:
            wall = Wall(x, y, width, height)
            wall.add(self.walls)

    def load_player(self, center_x, center_y, forward_angle):
        if self.player:
            self.player.kill()
        self.player = Player(center_x, center_y, forward_angle)

    def load(self):
        with open("static/maps/level%d.txt" % self.level, 'r') as fin:
            walls_cnt = int(fin.readline())
            walls = []
            for i in range(walls_cnt):
                x, y, width, height = map(int, fin.readline().split())
                walls.append((x, y, width, height))

            # 载入walls
            self.load_walls(walls)

            center_x, center_y, forward_angle = map(int, fin.readline().split())
            self.load_player(center_x, center_y, forward_angle)
    def check_collided(self):
        if pygame.sprite.spritecollide(self.player, self.walls, False, collided_rect):
            self.player.crash()

    def update(self):
        self.walls.update()
        self.walls.draw(self.screen)
        self.player.update()
        self.screen.blit(self.player.image, self.player.rect)


