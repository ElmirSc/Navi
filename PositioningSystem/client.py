import socket


# class to create a client to communicate to server
class Client:
    def __init__(self, ip, port):
        self.host_ip = ip  # host ip address
        self.port_number = port  # communication port
        self.connected_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = None
        self.connection = None
        self.address = None
        self.is_connected = False

    def connect_to_socket(self):  # function to create the client
        self.connected_client.settimeout(10)
        self.connected_client.connect((self.host_ip, self.port_number))
        self.is_connected = True

    def send_message(self, current_message_to_send):  # function to send messages to server
        self.connected_client.sendall(current_message_to_send.encode())

    def receive_message(self):  # function to receive messages
        try:
            self.data = self.connected_client.recv(1024)
            self.data = self.data.decode()
            print(self.data)
        except socket.timeout:
            print("No messages!")

    def close_connection(self):  # function to close the connection to server
        self.connected_client.close()
