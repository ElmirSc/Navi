import socket
import time


# class to create a client to communicate to server
class Client:
    def __init__(self):
        self.host_ip = '172.20.10.5'  # host ip address
        self.port_number = 5555  # communication port
        self.connected_client = None  # object which is the real socket
        self.data = None

    def create_socket(self):  # function to create the client
        self.connected_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_client.connect((self.host_ip, self.port_number))

    def send_message(self, current_message_to_send):  # function to send messages to server
        self.connected_client.sendall(current_message_to_send.encode())

    def receive_message(self):  # function to receive messages
        self.data = self.connected_client.recv(1024)

    def close_connection(self):  # function to close the connection to server
        self.connected_client.close()


def a_f_way(client):  # test function for route a -> f
    # client.create_socket()
    counter = 1
    speed = 0
    dist = 0.0
    rot = 4

    while True:
        client.create_socket()
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
        client.create_socket()
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


if __name__ == "__main__":
    # testing socket connection
    client = Client()
    a_f_way(client)
    # a_g_way(client)
    # client.create_socket()
    counter = 1
    speed = 0
    dist = 0
    rot = 4

    while True:
        client.create_socket()
        if dist == 2:
            rot = 1
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
