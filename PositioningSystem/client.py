import socket
import time


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
        self.connected_client.settimeout(0.01)
        self.connected_client.connect((self.host_ip, self.port_number))
        self.is_connected = True

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
    rot = 3

    while True:
        client.connect_to_socket()
        if dist > 2.0:
            rot = 1
        speed = speed + counter
        dist = dist + 0.5
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

def drive_a_b_way(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    while dist < 11.0:
        rot = 3
        if dist > 2.0 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        elif dist > 6.5 and check_for_rotation == 1:
            rot = 1
            check_for_rotation = 2
        #speed = speed + counter
        dist = dist + 0.3
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        if speed == 20:
            counter = -1
        elif speed == 0:
            counter = 1
        time.sleep(0.5)
        client.receive_message()
        print(client.data)

def a_b_way(client):  # test function for route a -> b
    # client.create_socket()
    while True:
        drive_a_b_way(client)
        input_of_tester = input("Want another round?[j/n]")
        if input_of_tester == "n":
            client.close_connection()
            break


if __name__ == "__main__":
    # testing socket connection
    client = Client("192.168.0.12", 5556)
    a_b_way(client)
