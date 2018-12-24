import enum
import pickle
import re
import socket
from threading import Thread

import my_message

movement_expression = r"^[nesoNSEO][1-9]?[0-9]*$"
building_expression = r"^[mpMP][nseoNSEO]$"
quit_expression = r"^[qQ]$"
commande_expression = "|".join(
    [movement_expression, building_expression, quit_expression])


class ClientCommand(enum.Enum):
    STOP_CLIENT = enum.auto()


@enum.unique
class ClientState(enum.Enum):
    WAITING = enum.auto()
    PLAYING = enum.auto()


class Client:
    def __init__(self):
        self.state = ClientState.WAITING

    def start_client(self):
        HOST = "127.0.0.1"
        PORT = 12800

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            while True:
                data = s.recv(1024)
                message = pickle.loads(data)

                if self.handle_message(message,
                                       s) is ClientCommand.STOP_CLIENT:

                    return

    def handle_message(self, message, socket):
        print(message.string_message)

        if message.message_type is my_message.MessageType.PLAY:
            self.state = ClientState.PLAYING
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
    Client.start_client()
