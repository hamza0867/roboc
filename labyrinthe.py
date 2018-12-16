# -*-coding:Utf-8 -*

import labyrinthe
import random
import robot
import string
"""Ce module contient la classe Labyrinthe."""

WALL = "O"
EXIT = "U"
DOOR = "."
ALPHABET = set(string.ascii_uppercase)
USED_SYMBOLS = {WALL, EXIT, DOOR}


def creer_labyrinthe_depuis_chaine(chaine):

    # we use split to get the lines of the maze
    # then we use list(string) to convert the string into a list of string
    # But the maze itself should be immutable, the maze doesn't change, so
    # we convert our list of lists of chars into a tuple of tuple of chars
    # to make sure our maze is immutable

    lines = chaine.split("\n")
    grille = [list(line) for line in lines]
    list_of_tuples = [tuple(l) for l in grille]
    tuple_of_tuples = tuple(list_of_tuples)

    return labyrinthe.Labyrinthe(tuple_of_tuples)


class Labyrinthe:
    """Classe représentant un labyrinthe."""

    def __init__(self, grille):
        self.robots = []
        self.grille = grille
        self.available_symbols = ALPHABET - USED_SYMBOLS

    def __str__(self):
        lines = [list(l) for l in self.grille]
        for rbt in self.robots:
            lines[rbt.x][rbt.y] = rbt.symbol
        lines = ["".join(line) for line in lines]
        return "\n".join(lines)

    def __grilleTupleToList__(self):
        """returns the grille in a list format"""
        return [list(l) for l in self.grille]

    def __listToTuple__(self, lst):
        return tuple(tuple(l) for l in lst)

    def moveUp(self, robot):
        if self.grille[robot.x - 1][robot.y] is not WALL:
            robot.moveUp()

    def moveDown(self, robot):
        if self.grille[robot.x + 1][robot.y] is not WALL:
            robot.moveDown()

    def moveLeft(self, robot):
        if self.grille[robot.x][robot.y - 1] is not WALL:
            robot.moveLeft()

    def moveRight(self, robot):
        if self.grille[robot.x][robot.y + 1] is not WALL:
            robot.moveRight()

    def addRobot(self):
        x = random.randint(1, len(self.grille) - 2)
        y = random.randint(1, len(self.grille[0]) - 2)

        while(self.grille[x][y] is WALL):
            x = random.randint(1, len(self.grille) - 2)
            y = random.randint(1, len(self.grille[0]) - 2)

        symbol = random.sample(self.available_symbols, 1)[0]
        self.available_symbols.remove(symbol)
        self.robots.append(robot.Robot(x, y, symbol))

    def __addRobotWithCoords__(self, x, y):
        """This methode was written to facilitate tests, not supposed
        to be used in the actual game"""
        self.robots.append(robot.Robot(x, y, 'X'))

    def wallUp(self, robot):
        if self.grille[robot.x - 1][robot.y] is DOOR:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x - 1][robot.y] = WALL
            self.grille = self.__listToTuple__(grille_list)

    def wallDown(self, robot):
        if self.grille[robot.x + 1][robot.y] is DOOR:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x + 1][robot.y] = WALL
            self.grille = self.__listToTuple__(grille_list)

    def wallRight(self, robot):
        if self.grille[robot.x][robot.y + 1] is DOOR:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x][robot.y + 1] = WALL
            self.grille = self.__listToTuple__(grille_list)

    def wallLeft(self, robot):
        if self.grille[robot.x][robot.y - 1] is DOOR:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x][robot.y - 1] = WALL
            self.grille = self.__listToTuple__(grille_list)

    def doorUp(self, robot):
        if self.grille[robot.x - 1][robot.y] is WALL:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x - 1][robot.y] = DOOR
            self.grille = self.__listToTuple__(grille_list)

    def doorDown(self, robot):
        if self.grille[robot.x + 1][robot.y] is WALL:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x + 1][robot.y] = DOOR
            self.grille = self.__listToTuple__(grille_list)

    def doorLeft(self, robot):
        if self.grille[robot.x][robot.y - 1] is WALL:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x][robot.y - 1] = DOOR
            self.grille = self.__listToTuple__(grille_list)

    def doorRight(self, robot):
        if self.grille[robot.x][robot.y + 1] is WALL:
            grille_list = self.__grilleTupleToList__()
            grille_list[robot.x][robot.y + 1] = DOOR
            self.grille = self.__listToTuple__(grille_list)
