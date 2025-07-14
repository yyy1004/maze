import pygame
import config
from player import Player
from game_manager import GameManager


pygame.init()
pygame.mixer.init()  # 初始化声音
screen = pygame.display.set_mode((config.SCREEN_WIDHT, config.SCREEN_EHIGHT))
clock = pygame.time.Clock()

success_time = -1  # -1表示当前没有获胜，否则表示获胜的时刻

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
    if success_time >= 0:
        if pygame.time.get_ticks() - success_time > 2000:  # 如果获胜后已经等待了2秒，则加载下一关
            has_next = game_manager.next_level()
            if not has_next:  # 如果没有下一关，则游戏结束
                success_finished = True
                continue
            success_time = -1  # 将获胜时间清空

    if game_manager.update():
        success_time = pygame.time.get_ticks()  # 更新获胜时刻

    # screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
