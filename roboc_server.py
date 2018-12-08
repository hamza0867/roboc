import os
import re
import select
import socket

import carte


def load_game():
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
        int(input("Entrez un numero de labyrinthe pour commencer a jouer : "))
        - 1].labyrinthe


def start_server():
    hote = ""
    port = 12800

    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(port))

    serveur_lance = True
    clients_connectes = []

    while serveur_lance:
        # On va vérifier que de nouveaux clients ne demandent pas à se connecter
        # Pour cela, on écoute la connexion_principale en lecture
        # On attend maximum 50ms
        connexions_demandees, wlist, xlist = select.select([connexion_principale],
                                                           [], [], 0.05)

        for connexion in connexions_demandees:
            connexion_avec_client, infos_connexion = connexion.accept()
            # On ajoute le socket connecté à la liste des clients
            clients_connectes.append(connexion_avec_client)

        # Maintenant, on écoute la liste des clients connectés
        # Les clients renvoyés par select sont ceux devant être lus (recv)
        # On attend là encore 50ms maximum
        # On enferme l'appel à select.select dans un bloc try
        # En effet, si la liste de clients connectés est vide, une exception
        # Peut être levée
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [],
                                                         0.05)
        except select.error:
            pass
        else:
            # On parcourt la liste des clients à lire

            for client in clients_a_lire:
                # Client est de type socket
            msg_recu = client.recv(1024)
            # Peut planter si le message contient des caractères spéciaux
            msg_recu = msg_recu.decode()
            execute_commade

            if msg_recu == "fin":
                stop_server()


def execute_commade(robot, commade):
    pass


def stop_server():
    serveur_lance = False
    print("Fermeture des connexions")

    for client in clients_connectes:
        client.close()


connexion_principale.close()
