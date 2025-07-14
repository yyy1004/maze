import pygame
import config
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, forward_angle):
        super().__init__()
        self.width = 100
        self.height = 50

        self.forward_angle = forward_angle  # 顺时针循环，初始向右
        # self.image = pygame.Surface((self.width, self.height))
        # self.image.fill("blue")
        self.image_source = pygame.image.load("static/images/car.png")
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))

        self.image = pygame.transform.rotate(self.image, -self.forward_angle)  # 新添加

        self.image.set_colorkey("black")

        self.rect = self.image.get_rect()
        #  self.rect.center = (config.SCREEN_WIDHT / 2, config.SCREEN_EHIGHT / 2)
        self.rect.center = (center_x, center_y)

        self.last_time = pygame.time.get_ticks()   # 毫秒
        self.delta_time = 0

        self.move_velocity_limit = 200
        self.move_velocity = 0
        self.move_acc = 600  # 每帧改变的位移
        self.friction = 0.9  # 摩擦力

        self.rotate_velocity = 0 # 转动速度
        self.rotate_velocity_limit = 140

    def update_delta_time(self):
        cur_time = pygame.time.get_ticks()
        self.delta_time = (cur_time - self.last_time) / 1000  # 单位改成秒
        self.last_time = cur_time

    def input(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_w]:
            self.move_velocity += self.move_acc * self.delta_time
            self.move_velocity = min(self.move_velocity, self.move_velocity_limit)

        elif key_pressed[pygame.K_s]:
            self.move_velocity -= self.move_acc * self.delta_time
            self.move_velocity = max(self.move_velocity, -self.move_velocity_limit)
        else:
            self.move_velocity = int(self.move_velocity * self.friction)

        if key_pressed[pygame.K_d]:
            self.rotate_velocity = self.rotate_velocity_limit
        elif key_pressed[pygame.K_a]:
            self.rotate_velocity = -self.rotate_velocity_limit
        else:
            self.rotate_velocity = 0

    def rotate(self, direction=1):
        self.forward_angle += self.rotate_velocity * self.delta_time * direction

        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("black")

        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, direction=1):
        # self.rect.x += self.move_velocity * self.delta_time

        if direction == 1 and abs(self.move_velocity) > 10:
            self.rotate(direction)

        vx = self.move_velocity * math.cos(math.pi * self.forward_angle / 180) * direction
        vy = self.move_velocity * math.sin(math.pi * self.forward_angle / 180) * direction

        self.rect.x += vx * self.delta_time
        self.rect.y += vy * self.delta_time

        if direction == -1 and abs(self.move_velocity) > 10: # 退回来的时候 先移动再转和前面相反
            self.rotate(direction)

    def crash(self):
        self.move(-1)  # 退回来
        self.move_velocity *= -1
        self.rotate_velocity *= -1

    def update(self):
        self.update_delta_time()
        self.input()
        self.move()


