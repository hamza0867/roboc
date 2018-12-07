# -*-coding: UTF-8 -*

import unittest

import labyrinthe


class TestLabyrinthe(unittest.TestCase):
    def setUp(self):

        self.chaine = """OOOOOOOOOO
O O    O O
O . OO   O
O O O    O
O OOOO O.O
O O O    U"""

        self.labyrinthe = labyrinthe.creer_labyrinthe_depuis_chaine(
            self.chaine)

    def test__str__(self):
        self.assertEqual(self.labyrinthe.__str__(), self.chaine)

    def test_addRobot(self):
        self.labyrinthe.addRobot()
        self.labyrinthe.addRobot()
        print(f"{self.labyrinthe}")
        self.assertTrue(self.labyrinthe.robots)

    def test_moveUP(self):
        self.labyrinthe.addRobot()
        old_x = self.labyrinthe.robots[0].x
        if (self.labyrinthe.grille[old_x - 1][self.labyrinthe.robots[0].y] is
                not labyrinthe.WALL):
            self.labyrinthe.moveUp(self.labyrinthe.robots[0])
            self.assertEqual(old_x - 1, self.labyrinthe.robots[0].x)
        else:
            print("test_moveUP failed because the robot can't move up")
