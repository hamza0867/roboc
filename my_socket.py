import socket


class ClientSocket():
    def __init__(self, sock=None, number=0):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.number = 0
        else:
            self.sock = sock
            self.number = number

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, message):
        self.sock.send(message)

    def recv(self, n_bytes):
        return self.sock.recv(n_bytes)

    def close(self):
        self.sock.close()
