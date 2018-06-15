class Settings():
    """存储外星人入侵的所有设置的类"""

    # 屏幕设置
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed_factor = 1
        self.ship_limit = 2

        # 子弹的设置
        self.bullet_speed_factor = 2
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 30

        # 外星人的设置
        self.alien_speed_factor = 5
        self.fleet_drop_speed = 50
        # fleet_direction为1表示向右，-1表示相左
        self.fleet_direction = -1

        # 以什么速度加快游戏节奏
        self.speed_scale = 1.2
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        """随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction为1表示向右，-1表示相左
        self.fleet_direction = 1

        # 积分
        self.alien_points = 5000

    def increase_speed(self):
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale
        self.alien_points = int(self.alien_points * self.speed_scale)
