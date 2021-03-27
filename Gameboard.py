import sys
from Towers import *
from enemy import *
from PyQt5.QtCore import Qt, QRectF, QBasicTimer, \
    pyqtSignal, QRect, QEvent, QObject
from PyQt5.QtGui import QBrush, QColor, QPainter, \
    QIcon, QPixmap, QFont, QImage, QMouseEvent, QCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QLabel, QLineEdit,
                             QPushButton, QDesktopWidget,
                             QFrame, QMessageBox)
from globals import *
import json


class GameEnd(QObject):
    victory = pyqtSignal()
    defeat = pyqtSignal()


class GameBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.interface = Interface(self)
        self.setCentralWidget(self.interface)

        self.setWindowTitle("Zerg Rush")
        self.setFixedSize(27 * squareSize, 20 * squareSize)
        self.center()
        self.last_clicked_button = None
        self.game = Game()
        self.setWindowIcon(QIcon(
            "{}Textures/Zergling.png".format(self.game.directory)))

        self.gamover = GameEnd()
        self.gamover.victory.connect(self.victory)
        self.gamover.defeat.connect(self.game_over)

        self.marine = QPushButton('Marine', self)
        self.marine.setGeometry(540, 480, 270, 30)
        self.marine.clicked.connect(self.buttonClicked)

        self.marauder = QPushButton('Marauder', self)
        self.marauder.setGeometry(540, 510, 270, 30)
        self.marauder.clicked.connect(self.buttonClicked)

        self.sensor_tower = QPushButton('Sensor Tower', self)
        self.sensor_tower.setGeometry(540, 540, 270, 30)
        self.sensor_tower.clicked.connect(self.buttonClicked)

        self.ghost = QPushButton('Ghost', self)
        self.ghost.setGeometry(540, 570, 270, 30)
        self.ghost.clicked.connect(self.buttonClicked)

        self.retail = QPushButton('Sell', self)
        self.retail.setGeometry(240, 480, 30, 30)
        self.retail.clicked.connect(self.sell_tower)

        self.mineralsBar = QLabel(self)
        self.mineralsBar.setText("Minerals: {}".
                                 format(str(self.game.minerals)))
        self.mineralsBar.setGeometry(610, 10, 210, 15)

        self.waveBar = QLabel(self)
        self.waveBar.setText("Wave: {}".format(str(self.game.wave)))
        self.waveBar.setGeometry(70, 10, 240, 10)

        self.levelBar = QLabel(self)
        self.levelBar.setText("Level: {}".format(str(self.game.level)))
        self.levelBar.setGeometry(10, 10, 60, 10)

        self.lives_bar = QLabel(self)
        self.lives_bar.setText("Lives: {}".format(str(self.game.lives)))
        self.lives_bar.setGeometry(310, 10, 300, 10)

        self.score_bar = QLabel(self)
        self.score_bar.setText("Score: {}".format(str(self.game.score)))
        self.score_bar.setGeometry(370, 10, 60, 10)

        self.timer = QBasicTimer()
        self.timer.start(gameSpeed, self)
        self.cursor_img = None
        self.default_button_color = self.marine.palette().button().color().getRgb()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def timerEvent(self, event):
        if self.interface.selected_item is not None and \
                        self.interface.selected_item.unit_type == "Tower":
            self.retail.setEnabled(True)
        else:
            self.retail.setEnabled(False)

        action = self.game.run()

        if action == 'Defeat':
            self.gamover.defeat.emit()
        elif action == 'Victory':
            self.gamover.victory.emit()
        elif action == 'Next wave':
            self.wave_manger()
        else:
            for tower in self.game.towers:
                if tower.no_image:
                    tower.place_an_image(self)
                tower.animate(self)

            for monster in self.game.monsters:
                if monster.no_image:
                    monster.place_an_image(self)
                monster.animate()

            self.change_score(self.game.score)
            self.debit_lives()

    def sell_tower(self):
        self.interface.selected_item.image.hide()
        self.game.sell_tower(self.interface.selected_item)
        self.interface.selected_item = None
        self.mineralsBar.setText("Minerals: {}".
                                 format(str(self.game.minerals)))

    def wave_manger(self):
        if not self.game.wave:
            for tower in self.game.towers:
                tower.image.hide()
            self.game.towers.clear()
        self.waveBar.setText("Wave: {}".format(str(self.game.wave)))
        self.levelBar.setText("Level: {}".format(str(self.game.level)))
        self.interface.enemyPath = self.game.enemy_path
        self.interface.update()

    def buttonClicked(self):
        sender = self.sender()
        if sender == self.marine:
            self.button_selected(self.marine,
                                 "{}Textures/MarineCursor.png".format(
                                     self.game.directory))
        elif sender == self.marauder:
            self.button_selected(self.marauder,
                                 "{}Textures/MarauderCursor.png".format(
                                     self.game.directory))
        elif sender == self.sensor_tower:
            self.button_selected(self.sensor_tower,
                                 "{}Textures/SensorTowerCursor.png".format(
                                     self.game.directory))
        else:
            self.button_selected(self.ghost,
                                 "{}Textures/GhostCursor.png".format(
                                     self.game.directory))

    def button_selected(self, button, cursor):
        if button.palette().button().color().getRgb() == self.default_button_color:
            button.setStyleSheet('background-color: #dddddd')
            self.setCursor(QCursor(QPixmap(cursor)))
            self.last_clicked_button = button
            self.cursor_img = cursor
        else:
            button.setStyleSheet('')
            self.last_clicked_button = None
            self.cursor_img = None
            self.unsetCursor()

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.last_clicked_button is None \
                and event.button() == Qt.LeftButton:
            self.show_info(x // squareSize, y // squareSize)
        else:
            if event.button() == Qt.LeftButton:
                x = x // squareSize * squareSize
                y = y // squareSize * squareSize
                if self.last_clicked_button == self.marine:
                    tower_name = 'Marine'
                elif self.last_clicked_button == self.ghost:
                    tower_name = 'Ghost'
                elif self.last_clicked_button == self.sensor_tower:
                    tower_name = 'Sensor Tower'
                else:
                    tower_name = "Marauder"
                result = self.game.build_tower(x, y, tower_name)
                if result:
                    self.debit_minerals(self.game.towers[-1].cost)
            elif self.last_clicked_button is not None:
                self.button_selected(self.last_clicked_button, "")
                self.last_clicked_button = None
                self.cursor_img = None
                self.unsetCursor()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton:
                if event.pos().y() >= squareSize * 16:
                    self.unsetCursor()
                elif self.cursor_img is not None \
                        and event.pos().y() > squareSize:
                    self.setCursor(QCursor(QPixmap(self.cursor_img)))
        return QMainWindow.eventFilter(self, source, event)

    def show_info(self, x, y):
        for monster in self.game.monsters:
            if x == monster.x // squareSize and y == monster.y // squareSize:
                self.interface.selected_item = monster
        for tower in self.game.towers:
            if x == tower.x // squareSize and y == tower.y // squareSize:
                self.interface.selected_item = tower
                break
            if tower.size == 2 * squareSize:
                if x == (tower.x // squareSize + 1) \
                        and y == tower.y // squareSize:
                    self.interface.selected_item = tower

    def debit_minerals(self, price):
        self.mineralsBar.setText("Minerals: {}".
                                 format(str(self.game.minerals)))

    def change_score(self, points):
        self.score_bar.setText("Score: {}".format(str(self.game.score)))

    def debit_lives(self):
        self.lives_bar.setText("Lives: {}".format(str(self.game.lives)))

    def victory(self):
        message = QMessageBox.question(self, 'Victory',
                                       "Congratz, Do you want to play again?",
                                       QMessageBox.Yes |
                                       QMessageBox.No, QMessageBox.Yes)
        if message == QMessageBox.Yes:
            self.restart()
        else:
            self.close()

    def game_over(self):
        message = QMessageBox.question(self, 'Defeat',
                                       "Game over, do you want to try again?",
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.Yes)
        if message == QMessageBox.Yes:
            self.restart()
        else:
            self.close()

    def restart(self):
        for tower in self.game.towers:
            tower.image.hide()
        for monster in self.game.monsters:
            monster.image.hide()
        self.game.restart()
        self.lives_bar.setText("Lives: {}".format(str(self.game.lives)))
        self.score_bar.setText("Score: {}".format(str(self.game.score)))
        self.mineralsBar.setText("Minerals: {}".
                                 format(str(self.game.minerals)))
        self.interface.enemyPath.clear()
        self.interface.selected_item = None
        self.interface.update()


class Game:

    def __init__(self):
        self.directory = sys.argv[0].replace('Gameboard.py', '')
        self.wave_completed = True
        self.time_to_wait = 5
        self.level = currentLevel
        self.wave = currentWave
        self.minerals = minerals
        self.lives = lives
        self.score = 0

        self.time_to_wait = 0
        self.monsters_to_spawn = []
        self.monsters = []
        self.towers = []
        self.bestiary = {Zergling.name: Zergling, Roach.name: Roach,
                         Mutalisk.name: Mutalisk}
        self.tower_catalouge = [Marine, Marauder, Ghost, SensorTower]
        self.enemy_path = []

    def restart(self):
        self.wave = -1
        self.level = 1
        self.minerals = 3000
        self.score = 0
        self.lives = 5
        self.monsters.clear()
        self.towers.clear()

    def sensor_tower_buff(self, x, y):
        for tower in self.towers:
            in_range = (pow(x - tower.x, 2) +
                        pow(y - tower.y, 2)) <= \
                       pow(SensorTower.shotrange, 2)
            if not tower.is_in_sensor_tower_range and in_range:
                tower.is_in_sensor_tower_range = True

    def build_tower(self, x, y, tower):
        x_squares = int(x / squareSize)
        y_squares = int(y / squareSize)
        result = False
        if x_squares < 27 and 0 < y_squares < 16:
            if map[x_squares, y_squares] is None \
                    or map[x_squares, y_squares]:
                if tower == "Marine" \
                        and self.minerals >= Marine.cost:
                    self.towers.append(Marine(x, y))
                    result = True
                if tower == "Ghost" \
                        and self.minerals >= Ghost.cost:
                    self.towers.append(Ghost(x, y))
                    result = True
                if tower == "Sensor Tower" \
                        and self.minerals >= SensorTower.cost:
                    self.towers.append(SensorTower(x, y))
                    result = True
                    self.sensor_tower_buff(x, y)
                if x_squares < 26 and y_squares < 16:
                    if map[x_squares+1, y_squares] is None \
                            and map[x_squares, y_squares] is None:
                        if tower == "Marauder" \
                                and self.minerals >= Marauder.cost:
                            self.towers.append(Marauder(x, y))
                            result = True
        if result:
            self.debit_minerals(self.towers[-1].cost)
        return result

    def debit_minerals(self, price):
        self.minerals -= price

    def change_score(self, points):
        self.score += points

    def debit_lives(self):
        self.lives -= 1

    def next_wave(self):
        try:
            level_folder = "{0}Levels/Level {1}/".format(
                self.directory, self.level)
            self.wave += 1
            with open("{}Waves.json".format(level_folder)) as outfile:
                data = json.load(outfile)
            with open("{}Path.json".format(level_folder)) as outfile:
                self.enemy_path = json.load(outfile)
                for cell in self.enemy_path:
                    map[cell[0], cell[1]] = False
            try:
                units = data[str(self.wave)]["Unit"]
                delay = int(data[str(self.wave)]["delay"])
                self.monsters_to_spawn = units
                self.time_to_wait = delay
            except KeyError:
                self.level += 1
                for cell in map:
                    map[cell[0], cell[1]] = None
                for tower in self.towers:
                    self.debit_minerals(-tower.cost)
                self.wave = -1
                self.score = 0
        except FileNotFoundError:
            return False
        return True

    def spawn(self, monster):
        self.monsters.append(monster())

    def sell_tower(self, tower):
        map[tower.x // squareSize, tower.y // squareSize] = True
        self.towers.remove(tower)
        self.debit_minerals(-tower.retailValue)

    def run(self):
        if not self.lives:
            return 'Defeat'

        if not self.monsters and self.time_to_wait < 1:
            if self.next_wave():
                return 'Next wave'
            else:
                return 'Victory'

        if not self.monsters:
            self.time_to_wait -= 1

        for monster in self.monsters:
            if monster.isFinished:
                self.debit_lives()
                self.monsters.remove(monster)
                continue
            elif monster.isDead:
                self.change_score(monster.points)
                self.debit_minerals(-monster.points)
                self.monsters.remove(monster)
            else:
                monster.move()

        for tower in self.towers:
            if tower.name == "Sensor Tower":
                self.sensor_tower_buff(tower.x, tower.y)

        for tower in self.towers:
            tower.attack(self)
            tower.is_in_sensor_tower_range = False

        for monster in self.monsters_to_spawn:
            if self.monsters_to_spawn[monster] != '0':
                self.spawn(self.bestiary[monster])
                self.monsters_to_spawn[monster] = \
                    str(int(self.monsters_to_spawn[monster]) - 1)
                break
        return 'Continue'


class Interface(QFrame):
    selected_item = None
    enemyPath = []

    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(0, 255, 0))
        painter.drawRect(0, 0, 900, 700)

        painter.setBrush(menuColour)
        painter.drawRect(0, 0, 600, 30)
        painter.drawRect(600, 0, 210, 30)
        painter.drawRect(300, 0, 300, 30)
        for i in range(3):
            painter.drawRect(i * 270, 480, 270, 120)

        painter.setBrush(grassColour)
        for i in range(27):
            for j in range(15):
                painter.drawRect(i * squareSize, (j + 1) *
                                 squareSize, squareSize, squareSize)

        painter.setBrush(pathColour)
        for sq in self.enemyPath:
            painter.drawRect(sq[0] * squareSize, sq[1] *
                             squareSize, squareSize, squareSize)

        if self.selected_item is not None:
            self.drawText(painter)

    def drawText(self, qp):
        if self.selected_item is not None:
            qp.setPen(QColor(0, 0, 255))
            if self.selected_item.size == squareSize:
                if self.selected_item.unit_type == "Tower" \
                        or not self.selected_item.isDead:
                    qp.drawEllipse(self.selected_item.x,
                                   self.selected_item.y, 30, 30)
            elif self.selected_item.size == squareSize * 2:
                qp.drawEllipse(self.selected_item.x,
                               self.selected_item.y - squareSize // 2,
                               60, 60)

        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Times New Roman', 16))

        if self.selected_item.unit_type == "Enemy":
            if not self.selected_item.isDead:
                qp.drawText(QRect(0, 495, 600, 300),
                            0, "Unit: {} \nHP {} \nType: {}".format(
                        self.selected_item.name,
                        str(self.selected_item.health),
                        self.selected_item.type))
        else:
            qp.drawText(QRect(0, 495, 600, 300),
                        0, "Tower: {} \nAttack: {} \nTargets: {}".format(
                self.selected_item.name,
                self.selected_item.damage_info,
                ', '.join(self.selected_item.can_attack)))

        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = GameBoard()
    mainWindow.show()
    app.installEventFilter(mainWindow)
    sys.exit(app.exec_())
