#!/usr/bin/env  python3

import enum
import os
import pickle
import re
import select
import socket
import sys

import carte
import labyrinthe
import my_message
import my_socket


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

    maze = cartes[
        int(input("Entrez un numero de labyrinthe pour commencer a jouer : "))
        - 1].labyrinthe

    return maze


def start_Server():
    HOST = "127.0.0.1"
    PORT = 12800
    maze = load_game()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        s.setblocking(False)
        clients = []

        while len(clients) < 2:
            clients.extend(connect_clients(s, maze))

        for conn in clients:
            message = my_message.Message(maze.__str__(),
                                         my_message.MessageType.MAZE)
            conn.send(pickle.dumps(message))

        while True:
            for conn in clients:
                if handle_player(conn, maze,
                                 conn.number) is ServerCommande.STOP_SERVER:
                    stop_server(clients, s)

                for conn in clients:
                    message = my_message.Message(maze.__str__(),
                                                 my_message.MessageType.MAZE)
                    conn.send(pickle.dumps(message))


def connect_clients(server_socket, maze):
    connected_clients = []
    clients, _, _ = select.select([server_socket], [], [], 0.05)
    player = len(maze.robots)

    for client in clients:
        conn, _ = client.accept()
        maze.addRobot()
        connected_clients.append(my_socket.ClientSocket(conn, player))
        message = ("client connected, your symbol is {}").format(
            maze.robots[player].symbol)
        mess = my_message.Message(message, my_message.MessageType.INFO)
        conn.send(pickle.dumps(mess))

        if len(maze.robots) < 2:
            mess = my_message.Message("waiting for other clients",
                                      my_message.MessageType.INFO)
            conn.send(pickle.dumps(mess))
        player += 1

    return connected_clients


def handle_player(conn, maze, player):
    message = my_message.Message("Your turn", my_message.MessageType.PLAY)
    conn.send(pickle.dumps(message))
    commande = conn.recv(1024).decode()

    if execute_commande(commande, maze, player) is ServerCommande.STOP_SERVER:
        return ServerCommande.STOP_SERVER


def execute_commande(commande, maze, player):

    movement_expression = r"^[nesoNSEO][1-9]?[0-9]*$"
    building_expression = r"^[mpMP][nseoNSEO]$"
    robot = maze.robots[player]

    if re.match(movement_expression, commande):
        return execute_movement_commade(commande, maze, robot)

    elif re.match(building_expression, commande):
        execute_building_commande(commande, maze, robot)
    elif commande in "Qq":
        # print(f"Merci pour avoir jouer a notre jeu")
        maze.robots.remove(robot)

        return ServerCommande.STOP_SERVER


# Helper functions #


class ServerCommande(enum.Enum):
    STOP_SERVER = enum.auto


def execute_movement_commade(commande, maze, robot):
    for i in range(0, int("".join(commande[1:])) if len(commande) > 1 else 1):

        if commande[0] == "n" or commande[0] == "N":
            maze.moveUp(robot)
        elif commande[0] == "s" or commande[0] == "S":
            maze.moveDown(robot)
        elif commande[0] == "o" or commande[0] == "O":
            maze.moveLeft(robot)
        elif commande[0] == "e" or commande[0] == "E":
            maze.moveRight(robot)

        if maze.grille[robot.x][robot.y] is labyrinthe.EXIT:
            return ServerCommande.STOP_SERVER


def execute_building_commande(commande, maze, robot):

    if commande[0] in "mM":
        if commande[1] in "nN":
            maze.wallUp(robot)
        elif commande[1] in "sS":
            maze.wallDown(robot)
        elif commande[1] in "eE":
            maze.wallRight(robot)
        elif commande[1] in "oO":
            maze.wallLeft(robot)
    elif commande[0] in "pP":
        if commande[1] in "nN":
            maze.doorUp(robot)
        elif commande[1] in "sS":
            maze.doorDown(robot)
        elif commande[1] in "eE":
            maze.doorRight(robot)
        elif commande[1] in "oO":
            maze.doorLeft(robot)


def stop_server(clients, sock_server):
    for client in clients:
        client.send(b"Game Over")
        client.close()
    sock_server.close()
    sys.exit(0)


if __name__ == "__main__":
    start_Server()
