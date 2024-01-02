import socket

class server:
    def __init__(self):
        self.host = '192.168.0.12'
        self.port = 5555
        self.server_socket = None
        self.connection = None
        self.address = None
        self.data = None
        self.dist = 0
        self.speed = 0
        self.rotation = 0

    def create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(10)
        self.server_socket.bind((self.host, self.port))
    def set_socket_to_listen_mode(self):
        self.server_socket.listen()

    def accept_connection(self):
        conn = 0
        addr = 0
        try:
            conn, addr = self.server_socket.accept()
            self.connection = conn
            self.address = addr
            return True
        except OSError as e:
            if isinstance(e, socket.timeout):
                return False


    def receive_data(self):
        self.data = self.connection.recv(1024)
        self.data = self.data.decode()


    def handle_data(self):
        if len(self.data) > 0:
            string = self.data.split()
            counter = 0
            for i in string:
                if i.isnumeric():
                    match counter:
                        case 0:
                            self.speed = int(i)
                            counter += 1
                        case 1:
                            self.dist = int(i)
                            counter += 1
                        case 2:
                            self.rotation = int(i)
                            counter += 1
                        case 3:
                            break

    def close_connection(self):
        self.server_socket.connection.close()


if __name__ == "__main__":
    server = server()
    server.create_socket()
    server.set_socket_to_listen_mode()
    while True:
        if server.accept_connection():
            print(f"Verbunden mit {server.address}")
            #while True:
            server.receive_data()
                #if not server.data:
                #    break
            server.handle_data()
            print("Speed: ", server.speed)
            print("Dist: ", server.dist)
        else:
            print("waiting for connection")
    server.connection.close()
