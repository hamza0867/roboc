# -*-coding:Utf-8 -*
"""Ce module contient la classe Robot."""


class Robot:
    """Classe representant un robot"""

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def moveUp(self):
        self.x -= 1

    def moveDown(self):
        self.x += 1

    def moveRight(self):
        self.y += 1

    def moveLeft(self):
        self.y -= 1
