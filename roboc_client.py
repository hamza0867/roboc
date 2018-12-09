import re
import socket


def start_client():
    HOST = "127.0.0.1"
    PORT = 12800

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        movement_expression = r"^[nesoNSEO][1-9]?[0-9]*$"
        building_expression = r"^[mpMP][nseoNSEO]$"
        quit_expression = r"^[qQ]$"
        commande_expression = "|".join(
            [movement_expression, building_expression, quit_expression])

        while True:
            maze = s.recv(1024).decode()
            print(maze)
            if maze == "Game Over":
                return
            commande = input("\n> ")

            while not re.match(commande_expression, commande):
                print(
                    "\nThe commande you typed does not exist, please type a valid\
                      commande")
                commande = input("\n> ")
            s.send(commande.encode())


if __name__ == "__main__":
    start_client()
