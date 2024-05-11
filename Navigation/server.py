import socket


# class which creates a socket an allows connections
class Server:
    def __init__(self,ip,port):
        self.host_ip = ip  # host ip address
        self.port_number = port  # communication port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # object which is the real socket
        self.connection = None
        self.address = None
        self.data = None
        self.driven_distance = 0
        self.distance_difference_between_cur_and_prev_values = 0
        self.current_speed = 0
        self.current_rotation = []
        self.has_connection_to_client = False
        self.fault_distance = 0

    def create_socket(self):  # function which creates and binds the socket with a timeout of 10sec
        self.server_socket.settimeout(20)
        self.server_socket.bind((self.host_ip, self.port_number))

    def set_socket_to_listen_mode(self):  # function to set the socket into listen mode
        self.server_socket.listen()

    def accept_connection(
            self):  # function to check if someone wants to communicate, after timeout there is an exception to let the code run
        try:
            print("trying to accept connection")
            conn, addr = self.server_socket.accept()
            self.connection = conn
            self.address = addr
            if self.connection is not None:
                self.has_connection_to_client = True
            return True
        except OSError as e:
            if isinstance(e, socket.timeout):
                return False

    def receive_data(self):  # function to receive data and decode it
        self.data = self.connection.recv(1024).decode()

    def handle_data(self):  # function to split every number of the data pack to get speed, distance and rotation
        if len(self.data) > 0:
            string = self.data.split()
            print(string)
            if len(string) > 0:
                self.current_speed = int(string[0])
                self.distance_difference_between_cur_and_prev_values = round((float(string[1]) - self.fault_distance) - self.driven_distance, 2)
                print("distance_diff:",self.distance_difference_between_cur_and_prev_values)
                self.driven_distance = float(string[1]) - self.fault_distance
                if int(string[2]) != 3:
                    self.current_rotation.append(int(string[2]))

    def close_connection(self):  # function to close the connection to other
        self.server_socket.connect.close()

    def send_data(self, data):
        data = self.change_data_into_string(data)
        if self.connection is not None:
            self.connection.sendall(data.encode())

    def change_data_into_string(self, data):
        data_to_send = ""
        if type(data) == int:
            return str(data)
        elif type(data) == str:
            return data
        for i in data:
            data_to_send = data_to_send + str(i) + " "
        return data_to_send


if __name__ == "__main__":
    server = Server("1.1.1.1", 4555)
    server.create_socket()
    server.set_socket_to_listen_mode()
    if server.accept_connection():
        #print(f"Verbunden mit {server.address}")
        while True:
            server.receive_data()
            print(server.data)

            server.send_data("hallo")
        else:
            print("waiting for connection")
    server.connection.close()
