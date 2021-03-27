from PyQt5.QtGui import QColor


minerals = 3000
score = 0
lives = 5
squareSize = 30
menuColour = QColor(117, 187, 253)
grassColour = QColor(1, 186, 17)
pathColour = QColor(10, 230, 10)

currentWave = -1

currentLevel = 1

isPaused = False

gameSpeed = 100

map = {(x, (y + 1)): None for x in range(27) for y in range(15)}
