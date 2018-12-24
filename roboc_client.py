import enum
import pickle
import re
import socket

import my_message

movement_expression = r"^[nesoNSEO][1-9]?[0-9]*$"
building_expression = r"^[mpMP][nseoNSEO]$"
quit_expression = r"^[qQ]$"
commande_expression = "|".join(
    [movement_expression, building_expression, quit_expression])


class ClientCommand(enum.Enum):
    STOP_CLIENT = enum.auto


def start_client():
    HOST = "127.0.0.1"
    PORT = 12800

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            data = s.recv(1024)
            message = pickle.loads(data)

            if handle_message(message, s) is ClientCommand.STOP_CLIENT:
                return


def handle_message(message, socket):
    if message.message_type in {
            my_message.MessageType.INFO,
            my_message.MessageType.MAZE,
    }:
        print(message.string_message)
    elif message.message_type is my_message.MessageType.PLAY:
        print("PLAY message made it")
        commande = input("\n> ")

        while not re.match(commande_expression, commande):
            print(
                "\nThe commande you typed does not exist, please type a valid\
                  commande")
            commande = input("\n> ")
        socket.send(commande.encode())
    elif message.message_type is my_message.MessageType.GAME_OVER:
        print("Game Over. See you next time !!")

        return ClientCommand.STOP_CLIENT


if __name__ == "__main__":
    start_client()
