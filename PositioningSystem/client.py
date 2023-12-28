import socket
class Client:
    def __init__(self):
        self.host = '172.20.10.5'
        self.port = 5555
        self.connected_client = None

    def create_socket(self):
        self.connected_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_client.connect((self.host, self.port))

    def send_message(self, message):
        self.connected_client.sendall(message.encode())


    def receive_message(self):
        data = self.connected_client.recv(1024)


    def close_connection(self):
        self.connected_client.close()

if __name__ == "__main__":
    client = Client()
    client.create_socket()
    client.send_message("Hallo vom Raspberry Pi!")
    client.send_message("Hallo vom Raspberry P2!")
    client.receive_message()
    client.close_connection()
