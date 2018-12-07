# -*-coding:Utf-8 -*
"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

import os
import re

import carte

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
    if nom_fichier.endswith(".txt"):
        chemin = os.path.join("cartes", nom_fichier)
        nom_carte = nom_fichier[:-3].lower()
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
            cartes.append(carte.Carte(nom_carte, contenu))

# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte_ in enumerate(cartes):
    print("  {} - {}".format(i + 1, carte_.nom))

# ... Complétez le programme ...
maze = cartes[
    int(input("Entrez un numero de labyrinthe pour commencer a jouer : ")) -
    1].labyrinthe

commande_expression = r"^[nesoNSEO][1-9]?[0-9]*$"


def game():
    while True:
        print(f"\n{maze}")
        commande = input("\n> ")
        if re.match(commande_expression, commande):
            for i in range(
                    0,
                    int("".join(commande[1:])) if len(commande) > 1 else 1):
                if commande[0] == "n" or commande[0] == "N":
                    maze.moveUp()
                elif commande[0] == "s" or commande[0] == "S":
                    maze.moveDown()
                elif commande[0] == "o" or commande[0] == "O":
                    maze.moveLeft()
                elif commande[0] == "e" or commande[0] == "E":
                    maze.moveRight()
                if maze.grille[maze.robot[0]][maze.robot[1]] == carte.EXIT:
                    print(f"Bravo vous avez gagne la partie")
                    return
        elif commande[0] == "q" or commande[0] == "Q":
            name = input(
                "\ncomment voulez vous nommer la partie qui sera sauvegarder: "
            )
            maze.save(name)
            return
        else:
            print(f"\nthe command {commande} that you entered does not exist")


game()
