import sys
import os
import math
from PyQt5.QtCore import Qt, QRectF, QBasicTimer, \
    pyqtSignal, QRect, QEvent, QObject
from PyQt5.QtGui import QBrush, QColor, QPainter, \
    QIcon, QPixmap, QFont, QImage, QMouseEvent, QCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QLabel, QLineEdit,
                             QPushButton, QDesktopWidget,
                             QFrame, QMessageBox, QComboBox)
from globals import map, grassColour, pathColour, \
    squareSize, menuColour
import json
from Levels import Level, Wave
import shutil


class Redactor(QMainWindow):

    def __init__(self):
        super(Redactor, self).__init__()
        self.interface = Interface(self)
        self.setCentralWidget(self.interface)
        self.setFixedSize(27 * squareSize, 20 * squareSize)
        self.setWindowTitle("Level Redactor")
        self.directory = sys.argv[0].replace('LevelRedactor.py', '')
        self.setWindowIcon(
            QIcon("{}Textures/Zergling.png".format(self.directory)))
        self.center()

        self.level = Level()
        self.wave = Wave()
        self.current_unit = "Zergling"
        self.current_wave = None
        self.current_level = None

        self.timer = QBasicTimer()
        self.timer.start(1000, self)
        self.add_level = QPushButton('Create', self)
        self.add_level.setGeometry(120, 510, 90, 30)
        self.add_level.clicked.connect(self.buttonClicked)

        self.edit_level = QPushButton('Edit', self)
        self.edit_level.setGeometry(120, 540, 90, 30)
        self.edit_level.clicked.connect(self.buttonClicked)

        self.remove_level = QPushButton('Delete', self)
        self.remove_level.setGeometry(120, 570, 90, 30)
        self.remove_level.clicked.connect(self.buttonClicked)

        self.wave_menu = QLabel(self)
        self.wave_menu.setText("Wave contains: ")
        self.wave_menu.move(550, 480)

        self.delay_label = QLabel(self)
        self.delay_label.setText("Delay: ")
        self.delay_label.move(660, 540)

        self.delay_input = QLineEdit(self)
        self.delay_input.setText("0")
        self.delay_input.setGeometry(660, 570, 90, 30)

        self.delay_set = QPushButton(self)
        self.delay_set.setGeometry(750, 570, 60, 30)
        self.delay_set.setText("Set")
        self.delay_set.clicked.connect(self.buttonClicked)

        self.wave_input = QLineEdit(self)
        self.wave_input.setGeometry(660, 510, 90, 30)
        self.wave_input.setText(str(self.wave.wave["Unit"][self.current_unit]))

        self.choose_level = QLabel(self)
        self.choose_level.setText("Choose the level: ")
        self.choose_level.move(10, 480)

        self.choose_wave = QLabel(self)
        self.choose_wave.setText("Choose the wave: ")
        self.choose_wave.move(280, 480)

        self.waves = QComboBox(self)
        self.waves.move(280, 510)
        self.waves.activated[str].connect(self.onActivated)

        self.units = QComboBox(self)
        self.units.addItems(["Zergling", "Mutalisk",
                             "Roach"])
        self.units.move(550, 510)
        self.units.activated[str].connect(self.onActivated)

        self.add_wave = QPushButton(self)
        self.add_wave.setGeometry(750, 510, 60, 30)
        self.add_wave.setText("Add")
        self.add_wave.clicked.connect(self.buttonClicked)

        self.delete_button = QPushButton(self)
        self.delete_button.setGeometry(390, 510, 60, 30)
        self.delete_button.setText("Delete")
        self.delete_button.clicked.connect(self.buttonClicked)

        self.levels = QComboBox(self)
        self.levels.move(10, 510)
        self.levels.addItem("None")
        self.levels.addItems(os.listdir("{}Levels/".format(self.directory)))
        self.levels.activated[str].connect(self.onActivated)
        self.path = []

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        x = event.pos().x() // squareSize
        y = event.pos().y() // squareSize
        if event.buttons() == Qt.LeftButton and x < 27 and 0 < y < 16:
            if not self.interface.enemyPath.__contains__([x, y]):
                self.interface.enemyPath.append([x, y])
        elif self.interface.enemyPath.__contains__([x, y]):
            self.interface.enemyPath.remove([x, y])

    def buttonClicked(self):
        sender = self.sender()
        if sender == self.add_level:
            self.add()
        elif sender == self.edit_level:
            self.edit()
        elif sender == self.remove_level:
            self.delete()
        elif sender == self.add_wave:
            self.wave.wave["Unit"][self.current_unit] = self.wave_input.text()
            self.waves.addItem(str(len(self.waves)))
            self.level.add_wave(self.wave)
            self.wave = Wave()
            self.wave_input.setText("0")
            self.delay_input.setText("0")
        elif sender == self.delay_set:
            self.wave.wave["delay"] = self.delay_input.text()
        elif sender == self.delete_button:
            if self.current_wave is not None:
                self.waves.removeItem(int(self.current_wave))
                self.level.delete_wave(int(self.current_wave))
                self.waves.clear()
                self.waves.addItems([str(x) for x in
                                     range(0, len(self.level.waves))])
                if self.level.waves:
                    self.wave.wave = self.level.waves['0']
                    self.delay_input.setText(
                        str(self.level.waves['0']["delay"]))
                    self.wave_input.setText(
                        str(self.level.waves['0']["Unit"][self.current_unit]))
                else:
                    self.wave.wave = Wave()
                    self.delay_input.setText('0')
                    self.wave_input.setText('0')

    def onActivated(self, text):
        sender = self.sender()
        if sender == self.units:
            self.wave.wave["Unit"][self.current_unit] = self.wave_input.text()
            self.wave_input.setText(str(self.wave.wave["Unit"][text]))
            self.current_unit = text
        elif sender == self.waves:
            self.wave.wave["Unit"][self.current_unit] = self.wave_input.text()
            self.delay_input.setText(str(self.level.waves[text]["delay"]))
            self.wave_input.setText(
                str(self.level.waves[text]["Unit"][self.current_unit]))
            self.wave.wave = self.level.waves[text]
            self.current_wave = text
        elif sender == self.levels:
            self.current_level = text
            try:
                self.waves.clear()
                with open(
                        "{0}Levels/{1}/Waves.json".format(
                            self.directory, text), 'r') \
                        as infile:
                    data = json.load(infile)
                self.level.waves = data
                self.wave.wave = data["0"]
                with open(
                        "{0}Levels/{1}/Path.json".format(
                            self.directory, text), 'r') \
                        as infile:
                    enemy_path = json.load(infile)
                self.interface.enemyPath = enemy_path
                for key in data:
                    self.waves.addItem(key)
                self.wave_input.setText(
                    str(self.level.waves["0"]["Unit"][self.current_unit]))
            except FileNotFoundError:
                self.level = Level()
                self.interface.enemyPath = []
                self.waves.clear()
                self.wave = Wave()
                self.wave_input.setText("0")
            self.delay_input.setText(str(self.wave.wave["delay"]))

    def add(self):
        if self.check_path() and self.check_info():
            level_number = len(
                os.listdir("{}Levels/".format(self.directory))) + 1
            self.make_level_dir(level_number)
        else:
            reply = QMessageBox.question(self, 'Message', "Wrong input",
                                         QMessageBox.Ok, QMessageBox.Ok)

    def edit(self):
        if self.current_level is not None \
                and self.check_path() \
                and self.check_info() \
                and self.current_level in os.listdir(
                    "{}Levels/".format(self.directory)):
            self.dump_level_info()
        else:
            reply = QMessageBox.question(self, 'Message', "Wrong input",
                                         QMessageBox.Ok, QMessageBox.Ok)

    def delete(self):
        if self.current_level is not None:
            level_number = self.current_level[-1]
            shutil.rmtree('{0}Levels/{1}'.format(
                self.directory, self.current_level))
            for folder in os.listdir("{}Levels/".format(self.directory)):
                if folder[-1] > level_number[-1]:
                    os.rename('{0}Levels/{1}'.format(
                        self.directory, folder), "{} {}".format(
                        "Level", str(int(folder[-1]) - 1)))
            self.levels.clear()
            self.levels.addItem("None")
            self.levels.addItems(
                os.listdir("{}Levels/".format(self.directory)))
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Choose a level to delete",
                                         QMessageBox.Ok, QMessageBox.Ok)

    def make_level_dir(self, level_number):
        os.mkdir("{0}Levels/Level {1}".format(
            self.directory, str(level_number)))
        self.current_level = 'Level {}'.format(level_number)
        self.dump_level_info()
        self.levels.addItem("Level {}".format(str(level_number)))

    def dump_level_info(self):
        with open('{0}Levels/{1}/Waves.json'.format(
                self.directory, self.current_level), 'w') as outfile:
            json.dump(self.level.waves, outfile)
        with open('{0}Levels/{1}/Path.json'.format(
                self.directory, self.current_level), 'w') as outfile:
            json.dump(self.path, outfile)

    def check_info(self):
        for wave in self.level.waves:
            if not self.is_int(self.level.waves[wave]["delay"]):
                return False

            for unit in self.level.waves[wave]["Unit"]:
                if not self.is_int(self.level.waves[wave]["Unit"][unit]):
                    return False
        return self.level.waves

    def is_int(self, a):
        try:
            int(a)
            return int(a) >= 0
        except ValueError:
            return a.isdigit() \
                   and ((a[0] != "0" and len(a) > 1) or len(a) == 1)

    def check_path(self):
        self.path = []
        self.end_is_reachable = False
        self.cells_that_can_be_the_start = []
        for cell in self.interface.enemyPath:
            if self.can_be_start(cell):
                self.cells_that_can_be_the_start.append(cell)
        if not len(self.cells_that_can_be_the_start) == 1:
            return False
        self.move_to_next_cell(self.cells_that_can_be_the_start[0])
        return \
            self.end_is_reachable \
            and self.cells_connected() \
            and len(self.path) == len(self.interface.enemyPath)

    def can_be_start(self, cell):
        cells = 0
        for i in range(0, 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if self.interface.enemyPath.__contains__([i, j]) \
                        and math.fabs(cell[0] - i + cell[1] - j) == 1:
                    cells += 1
        return cell[0] == 0 and cells == 1

    def move_to_next_cell(self, cell):
        if not self.end_is_reachable:
            self.path.append(cell)
        else:
            return
        if cell[0] == 26:
            self.end_cell = cell
            self.end_is_reachable = True
        for square in self.interface.enemyPath:
            if math.fabs(cell[0] - square[0] + cell[1] - square[1]) == 1 \
                    and not self.path.__contains__(square) \
                    and math.fabs(cell[0] - square[0]) < 2 \
                    and math.fabs(cell[1] - square[1]) < 2:
                self.move_to_next_cell(square)

    def cells_connected(self):
        for cell in self.interface.enemyPath:
            if cell != self.cells_that_can_be_the_start[0] \
                    and cell != self.end_cell:
                close_cells = 0
                for i in range(cell[0] - 1, cell[0] + 2):
                    for j in range(cell[1] - 1, cell[1] + 2):
                        if self.interface.enemyPath.__contains__([i, j]) \
                                and math.fabs(cell[0] - i + cell[1] - j) == 1:
                            close_cells += 1
                if close_cells != 2:
                    return False
        return True


class Interface(QFrame):
    enemyPath = []

    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(0, 255, 0))
        painter.drawRect(0, 0, 900, 700)

        painter.setBrush(menuColour)
        painter.drawRect(0, 0, 810, 30)
        for i in range(3):
            painter.drawRect(i * 270, 480, 270, 120)

        painter.setBrush(grassColour)
        for i in range(27):
            for j in range(15):
                painter.drawRect(i * squareSize,
                                 (j + 1) * squareSize, squareSize, squareSize)

        painter.setBrush(pathColour)
        for cell in self.enemyPath:
            painter.drawRect(cell[0] * squareSize,
                             cell[1] * squareSize, squareSize, squareSize)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Redactor()
    mainWindow.show()
    sys.exit(app.exec_())
