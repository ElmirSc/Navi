import socket


class Server:
    def __init__(self):
        self.host_ip = '192.168.0.12'
        self.port_number = 5555
        self.server_socket = None
        self.connection = None
        self.address = None
        self.data = None
        self.driven_distance = 0
        self.current_speed = 0
        self.current_rotation = 0

    def create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(10)
        self.server_socket.bind((self.host_ip, self.port_number))

    def set_socket_to_listen_mode(self):
        self.server_socket.listen()

    def accept_connection(self):
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

            if len(string) > 0:
                self.current_speed = int(string[0])
                self.driven_distance = float(string[1])
                self.current_rotation = int(string[2])

    def close_connection(self):
        self.server_socket.connection.close()


if __name__ == "__main__":
    server = Server()
    server.create_socket()
    server.set_socket_to_listen_mode()
    while True:
        if server.accept_connection():
            print(f"Verbunden mit {server.address}")
            # while True:
            server.receive_data()
            # if not server.data:
            #    break
            server.handle_data()
            print("Speed: ", server.current_speed)
            print("Dist: ", server.driven_distance)
        else:
            print("waiting for connection")
    server.connection.close()
