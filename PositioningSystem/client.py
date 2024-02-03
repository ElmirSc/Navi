import socket
import time


# class to create a client to communicate to server
class Client:
    def __init__(self):
        self.host_ip = '172.20.10.5'  # host ip address
        self.port_number = 5556  # communication port
        self.connected_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = None
        self.connection = None
        self.address = None

    def connect_to_socket(self):  # function to create the client
        self.connected_client.settimeout(0.001)
        self.connected_client.connect((self.host_ip, self.port_number))

    def send_message(self, current_message_to_send):  # function to send messages to server
        self.connected_client.sendall(current_message_to_send.encode())

    def receive_message(self):  # function to receive messages
        try:
            self.data = self.connected_client.recv(1024)
            self.data = self.data.decode()
        except socket.timeout:
            print("No messages!")

    def close_connection(self):  # function to close the connection to server
        self.connected_client.close()

    def accept_connection(
            self):  # function to check if someone wants to communicate, after timeout there is an exception to let the code run
        try:
            conn, addr = self.connected_client.accept()
            self.connection = conn
            self.address = addr
            return True
        except OSError as e:
            if isinstance(e, socket.timeout):
                return False

    def set_socket_to_listen_mode(self):  # function to set the socket into listen mode
        self.connected_client.listen()


def a_f_way(client):  # test function for route a -> f
    # client.create_socket()
    counter = 1
    speed = 0
    dist = 0.0
    rot = 4

    while True:
        client.connect_to_socket()
        if dist > 2.0:
            rot = 1
        speed = speed + counter
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        client.close_connection()
        if speed == 20:
            counter = -1
        elif speed == 0:
            counter = 1
        time.sleep(0.5)


def a_g_way(client):  # test function for route a -> g
    # client.create_socket()
    counter = 1
    speed = 0
    dist = 0
    rot = 4
    while True:
        client.connect_to_socket()
        if dist == 5:
            rot = 0
        speed = speed + counter
        dist = dist + counter
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        client.close_connection()
        if speed == 20:
            counter = -1
        elif speed == 0:
            counter = 1
        time.sleep(4)

def a_b_way(client):  # test function for route a -> b
    # client.create_socket()
    counter = 1
    speed = 0
    dist = 0.0
    rot = 4
    client.connect_to_socket()
    while dist < 11.0:
        rot = 3
        if dist > 2.0 and dist < 6.5:
            rot = 1
        elif dist > 6.5:
            rot = 2
        speed = speed + counter
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #client.close_connection()
        if speed == 20:
            counter = -1
        elif speed == 0:
            counter = 1
        time.sleep(0.5)
    client.close_connection()


if __name__ == "__main__":
    # testing socket connection
    client = Client()
    #client.create_socket()
    #client.send_message("Test")
    #client.set_socket_to_listen_mode()
    #while True:
        #if client.accept_connection():
    #client.receive_message()
    #print(client.data)
    #client.close_connection()
    a_b_way(client)
    # a_g_way(client)
    # client.create_socket()