import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """相应按键"""

    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True

    elif event.key == pygame.K_UP:
        # 向上移动飞船
        ship.moving_up = True

    elif event.key == pygame.K_DOWN:
        # 向下移动飞船
        ship.moving_down = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """相应按键"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        # 向上移动飞船
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        # 向下移动飞船
        ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship,
                              ai_settings, screen, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship,
                      ai_settings, screen, sb):
    """玩家点击play开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏相关设置
        ai_settings.initialize_dynamic_setting()
        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置积分类图像
        sb.prep_high_score()
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    """更新屏幕图像，并切换到屏幕"""
    # 每次循环都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullet(ai_settings, screen, bullets, aliens, ship, stats, sb):
    """更新子弹位置，并删除消失的子弹"""
    # 更新子弹位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets,stats, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一个子弹，并将其加入到编组bullects中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_alien_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - (alien_width * 2)
    number_alien_x = int(available_space_x / (alien_width * 2))
    return number_alien_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕能够容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         3 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x

    alien.rect.y = alien.rect.height + 2 * alien_height * row_number
    alien.add(aliens)


def create_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群"""
    # 创建一个外星人，计算一行可以容纳多少外星人
    # 外星人的间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_alien_y = get_number_rows(ai_settings, ship.rect.width,
                                     alien.rect.width)
    # 创建第一行外星人
    for row_number in range(number_alien_y):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_buttom(ai_settings, screen, aliens, ship, bullets, stats, sb)
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb)



def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets, stats, sb):

    # 检查是否有子弹命中了外星人
    # 若果有，删除对应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    check_high_score(stats, sb)
    if len(aliens) == 0:
        ai_settings.increase_speed()
        # 删除现有子弹并新建一群外星人
        bullets.empty()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)

def ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb):
    """响应被外星人撞到的飞船"""
    # 将ships_left减1
    if stats.ships_left > 1:
        stats.ships_left -= 1

        sb.prep_ships()

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 新建外星人，并将飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()



        # 暂停0.5s
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_buttom(ai_settings, screen, aliens, ship, bullets, stats, sb):
    """检查是不是有敌人到达了底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb)
            break

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()