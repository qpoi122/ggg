import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from scoreboard import Scoreboard
from game_stats import GameStats
from button import Button
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Ailen Invasion")

    # 创建一个用于统计储存信息的实例
    stats = GameStats(ai_settings)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建外星人
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # 创建play 按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建游戏统计实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_settings, screen, bullets, aliens, ship, stats, sb)
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb)


run_game()
