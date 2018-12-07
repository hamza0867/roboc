# -*-coding:Utf-8 -*
import labyrinthe

"""Ce module contient la classe Carte."""


class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, chaine):
        self.nom = nom
        self.labyrinthe = labyrinthe.creer_labyrinthe_depuis_chaine(chaine)

    def __repr__(self):
        return f"<Carte {self.nom}>"

