import socket
import time
class client:
    def __init__(self):
        self.host = '192.168.0.12'
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
    #testing socket connection
    client = client()
    #client.create_socket()
    counter = 1
    speed = 0
    dist = 0
    rot = 1
    while True:
        client.create_socket()
        speed = speed + counter
        dist = dist + counter
        message = str(speed)+" "+str(dist)+" "+str(rot)
        print(dist)
        client.send_message(message)
        client.close_connection()
        if speed == 20:
            counter = -1
        elif speed == 0:
            counter = 1
        time.sleep(4)

