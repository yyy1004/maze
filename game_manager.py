import pygame
from wall import Wall
from player import Player
from star import  Star
from target import Target
from utils.crash_collide import collided_rect, collided_circle


class GameManager:
    def __init__(self, screen, level=1):
        self.screen = screen
        self.level = level

        self.player = None
        self.walls = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self.eat_stars_sound = pygame.mixer.Sound("static/sounds/eat_stars.wav")
        self.eat_stars_sound.set_volume(0.3)
        self.success_sound = pygame.mixer.Sound("static/sounds/success.wav")
        self.success_sound.set_volume(0.3)

        self.stars_cnt = 0
        self.targets = pygame.sprite.Group()

        self.load()

    def load_walls(self, walls):
        self.walls.empty()
        for x, y, width, height in walls:
            wall = Wall(x, y, width, height)
            wall.add(self.walls)
    def load_stars(self, stars):
        self.stars.empty()
        for x, y in stars:
            star = Star(x, y)
            star.add(self.stars)

    def load_targets(self, targets):
        self.targets.empty()
        for x, y in targets:
            target = Target(x, y)
            target.add(self.targets)
    def load_player(self, center_x, center_y, forward_angle):
        if self.player:
            self.player.kill()
        self.player = Player(center_x, center_y, forward_angle)



    def load(self):  # 加载地图信息
        with open("static/maps/level%d.txt" % self.level, 'r') as fin:
            walls_cnt = int(fin.readline())
            walls = []
            for i in range(walls_cnt):
                x, y, width, height = map(int, fin.readline().split())
                walls.append((x, y, width, height))

            # 载入walls
            self.load_walls(walls)
            self.stars_cnt = int(fin.readline())
            starts = []
            for i in range(self.stars_cnt):
                x, y = map(int, fin.readline().split())
                starts.append((x, y))
            self.load_stars(starts)

            targets_cnt = int(fin.readline())
            targets = []
            for i in range(targets_cnt):
                x, y = map(int, fin.readline().split())
                targets.append((x, y))
            self.load_targets(targets)

            center_x, center_y, forward_angle = map(int, fin.readline().split())
            self.load_player(center_x, center_y, forward_angle)

    #  检测碰撞
    def check_collided(self):
        if pygame.sprite.spritecollide(self.player, self.walls, False, collided_rect):
            self.player.crash()
        if pygame.sprite.spritecollide(self.player, self.stars, True, collided_circle):
            self.stars_cnt -= 1
            self.eat_stars_sound.play()
        if self.stars_cnt == 0:
            if pygame.sprite.spritecollide(self.player, self.targets, True, collided_circle):
                self.success_sound.play()
                return True  # 获胜
        return False
    def update(self):
        self.stars.update()
        self.stars.draw(self.screen)
        self.targets.update()
        self.targets.draw(self.screen)

        self.walls.update()
        self.check_collided()
        self.walls.draw(self.screen)
        self.player.update()
        self.screen.blit(self.player.image, self.player.rect)


