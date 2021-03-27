from globals import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Enemy(object):
    x = None
    y = None
    no_image = True

    def __init__(self):
        self.isFinished = False
        self.isDead = False
        self.size = squareSize
        self.picture = None
        self.unit_type = "Enemy"
        self.number_of_the_current_block = 0
        self.enemyPath = []
        no_image = True

    def move(self):
        if len(self.enemyPath):
            if self.current_block == self.enemyPath[len(self.enemyPath) - 1]:
                self.isFinished = True
                self.checkHP()

        if not self.isDead and not self.isFinished:
            self.checkHP()
            self.current_block = \
                self.enemyPath[self.number_of_the_current_block + 1]
            self.number_of_the_current_block += 1
            self.x = \
                self.enemyPath[self.number_of_the_current_block][0] * \
                squareSize
            self.y = \
                self.enemyPath[self.number_of_the_current_block][1] * \
                squareSize

    def animate(self):
        if self.isDead:
            self.image.hide()
        if self.x is not None:
            self.image.move(self.x, self.y)

    def checkHP(self):
        if self.health <= 0 or self.isFinished:
            self.isDead = True
            self.x = None
            self.y = None

    def place_an_image(self, gameBoard):
        self.enemyPath = gameBoard.interface.enemyPath
        self.x = self.enemyPath[0][0] * squareSize
        self.y = self.enemyPath[0][1] * squareSize
        self.current_block = self.enemyPath[0]
        self.image = QLabel(gameBoard)
        self.image.setPixmap(QPixmap("{0}{1}".format(gameBoard.game.directory,
                                                     self.picture)))
        self.image.move(self.x, self.y)
        self.image.show()
        self.no_image = False


class Zergling(Enemy):
    name = "Zergling"
    type = "ground"
    health = 100
    points = 50

    def __init__(self):
        super(Zergling, self).__init__()
        self.picture = "Textures/Ling.png"


class Roach(Enemy):
    name = "Roach"
    type = "ground"
    health = 200
    points = 75

    def __init__(self):
        super(Roach, self).__init__()
        self.picture = "Textures/Roach.png"


class Mutalisk(Enemy):
    name = "Mutalisk"
    type = "air"
    health = 150
    points = 75

    def __init__(self):
        super(Mutalisk, self).__init__()
        self.picture = "Textures/Mutalisk.png"
