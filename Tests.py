from LevelRedactor import *
from Gameboard import *
from Towers import *
from enemy import *
import unittest


class TestLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Game()

    def test_spawn(self):
        self.game.spawn(Zergling)
        self.assertEqual(1, len(self.game.monsters))

    def test_sell_tower(self):
        self.game.build_tower(30, 60, 'Marine')
        self.game.sell_tower(self.game.towers[0])
        self.assertTrue(len(self.game.towers) == 1)

    def test_build_tower(self):
        self.game.build_tower(30, 90, "Marine")
        self.assertEqual(self.game.towers[0].name, 'Marine')

    def test_debit_minerals(self):
        self.game.debit_minerals(300)
        self.assertEqual(self.game.minerals, 2600)

    def test_change_score(self):
        self.game.change_score(2)
        self.assertEqual(self.game.score, 2)

    def test_debit_lives(self):
        lives = self.game.lives
        self.game.debit_lives()
        self.assertEqual(lives - 1, self.game.lives)

    def test_sensor_tower_buff(self):
        self.game.build_tower(90, 60, 'Marine')
        self.game.build_tower(90, 90, 'Sensor Tower')
        self.assertTrue(self.game.towers[0].is_in_sensor_tower_range)


class TestMonsters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Game()
        cls.monster = Zergling()

    def test_move(self):
        self.monster.health = 1
        self.monster.isDead = False
        self.monster.enemyPath = [[0, 8], [1, 8], [1, 7],
                                  [2, 7], [3, 7], [3, 6],
                                  [3, 5], [3, 4], [3, 3],
                                  [4, 3], [5, 3], [5, 4],
                                  [5, 5], [5, 6], [5, 7],
                                  [6, 7], [6, 8], [6, 9],
                                  [6, 10], [6, 11], [6, 12],
                                  [7, 12], [8, 12], [8, 11],
                                  [8, 10], [8, 9], [8, 8],
                                  [8, 7], [9, 7], [10, 7],
                                  [10, 8], [11, 8], [11, 9],
                                  [12, 9], [13, 9], [13, 8],
                                  [13, 7], [14, 7], [15, 7],
                                  [15, 8], [15, 9], [16, 9],
                                  [17, 9], [17, 8], [17, 7],
                                  [18, 7], [19, 7], [19, 8],
                                  [20, 8], [21, 8], [21, 7],
                                  [22, 7], [23, 7], [23, 8],
                                  [24, 8], [25, 8], [26, 8]]
        self.monster.current_block = self.monster.enemyPath[0]
        self.monster.move()
        self.assertFalse([0, 8] == self.monster.current_block)

    def test_checkHP(self):
        self.monster.health = 0
        self.monster.checkHP()
        self.assertTrue(self.monster.isDead)


class TestTowers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Game()
        cls.tower = Marine(30, 60)

    def test_deal_damage(self):
        monster = Zergling()
        monster.enemyPath = [[0, 8], [1, 8], [1, 7],
                             [2, 7], [3, 7], [3, 6],
                             [3, 5], [3, 4], [3, 3],
                             [4, 3], [5, 3], [5, 4],
                             [5, 5], [5, 6], [5, 7],
                             [6, 7], [6, 8], [6, 9],
                             [6, 10], [6, 11], [6, 12],
                             [7, 12], [8, 12], [8, 11],
                             [8, 10], [8, 9], [8, 8],
                             [8, 7], [9, 7], [10, 7],
                             [10, 8], [11, 8], [11, 9],
                             [12, 9], [13, 9], [13, 8],
                             [13, 7], [14, 7], [15, 7],
                             [15, 8], [15, 9], [16, 9],
                             [17, 9], [17, 8], [17, 7],
                             [18, 7], [19, 7], [19, 8],
                             [20, 8], [21, 8], [21, 7],
                             [22, 7], [23, 7], [23, 8],
                             [24, 8], [25, 8], [26, 8]]
        health = monster.health
        self.tower.deal_damage(monster)
        self.assertTrue(health > monster.health)


if __name__ == '__main__':
    unittest.main()
