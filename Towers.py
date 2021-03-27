from globals import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer
import math


class Tower(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.center = None
        self.unit_type = "Tower"
        self.no_image = True
        self.monster_x = None
        self.monster_y = None

    def move_to_the_center_of_block(self, x, y):
        corner_x = int(x/squareSize)
        corner_y = int(y/squareSize)
        self.center = [corner_x * squareSize + squareSize // 2,
                       corner_y * squareSize + squareSize // 2]
        if self.size == squareSize:
            map[corner_x, corner_y] = False
            self.image.move(corner_x * squareSize, corner_y * squareSize)
        elif self.size == squareSize * 2:
            map[corner_x, corner_y] = False
            map[corner_x + 1, corner_y] = False
            self.image.move(corner_x * squareSize, corner_y * squareSize)

    def place_an_image(self, gameboard):
        picture = "{0}{1}".format(gameboard.game.directory, self.picture)
        self.image = QLabel(gameboard)
        self.image.setPixmap(QPixmap(picture))
        self.move_to_the_center_of_block(self.x, self.y)
        self.image.show()
        self.no_image = False

    def animate(self, gameBoard):
        if self.monster_x is not None:
            self.shot_timer = QTimer()
            self.shot = QLabel(gameBoard)
            self.shot_stage = 0
            self.shot.setPixmap(QPixmap("{}Textures/Shot.png".format(
                gameBoard.game.directory)))
            self.shot_timer.timeout.connect(lambda: self.move_shot())
            self.shot_timer.start(gameSpeed // 10)
            self.shot.show()
            self.shot.move(self.x, self.y)

    def attack(self, game):
        self.monster_x = None
        self.monster_y = None
        for monster in game.monsters:
            if not monster.isFinished \
                    and (pow(self.x - monster.x, 2) +
                         pow(self.y - monster.y, 2)) <= pow(
                        self.shotrange, 2) \
                    and monster.type in self.can_attack:
                self.monster_x = monster.x
                self.monster_y = monster.y
                self.deal_damage(monster)
                break

    def move_shot(self):
        if not self.shot_stage:
            self.shot.move((self.x + self.monster_x) // 2,
                           (self.y + self.monster_y) // 2)
            self.shot_stage += 1
        elif self.shot_stage == 1:
            self.shot.move(self.monster_x, self.monster_y)
            self.shot_stage += 1
        elif self.shot_stage == 2:
            self.shot.hide()
            self.shot_stage = 0
            self.shot_timer.stop()


class Marine(Tower):
    name = "Marine"
    cost = 100
    size = squareSize
    shotrange = 60
    damage = 50
    damage_info = "50"
    retailValue = 75
    can_attack = ["ground", "air"]
    is_in_sensor_tower_range = False
    picture = "Textures/Marine.png"

    def __init__(self, x, y):
        super(Marine, self).__init__(x, y)

    def deal_damage(self, monster):
        if self.is_in_sensor_tower_range:
            monster.health -= self.damage * 1.5
        else:
            monster.health -= self.damage


class Marauder(Tower):
    name = "Marauder"
    size = 2 * squareSize
    shotrange = 60
    cost = 200
    damage = 10
    damage_info = "10 + 25% monster's HP"
    retailValue = 150
    can_attack = ["ground"]
    is_in_sensor_tower_range = False
    picture = "Textures/Marauder.png"

    def __init__(self, x, y):
        super(Marauder, self).__init__(x, y)

    def deal_damage(self, monster):
        if self.is_in_sensor_tower_range:
            monster.health -= (self.damage + monster.health // 100 * 25) * 1.2
        else:
            monster.health -= self.damage + monster.health // 100 * 25


class Ghost(Tower):
    name = "Ghost"
    size = squareSize
    shotrange = 60
    cost = 150
    damage = 10
    damage_info = "10 + distance / 2"
    retailValue = 110
    can_attack = ["ground", "air"]
    is_in_sensor_tower_range = False
    picture = "Textures/Ghost.png"

    def __init__(self, x, y):
        super(Ghost, self).__init__(x, y)

    def deal_damage(self, monster):
        if self.is_in_sensor_tower_range:
            monster.health -= self.damage + \
                              math.sqrt(pow((self.x - monster.x), 2) +
                                        pow((self.y - monster.y), 2)) // \
                              2 * 1.2
        else:
            monster.health -= self.damage + \
                              math.sqrt(pow((self.x - monster.x), 2) +
                                        pow((self.y - monster.y), 2)) // 2


class SensorTower(Tower):
    name = "Sensor Tower"
    size = squareSize
    shotrange = 100
    cost = 400
    damage = 0
    damage_info = "Does not attack"
    retailValue = 175
    can_attack = ["none"]
    is_in_sensor_tower_range = True
    picture = "Textures/Sensor_tower.png"

    def __init__(self, x, y):
        super(SensorTower, self).__init__(x, y)

    def deal_damage(self, monster):
        return
