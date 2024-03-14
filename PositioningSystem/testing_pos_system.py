from client import Client
import time


def drive_a_b_way(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    while dist < 14.0:
        rot = 3
        if dist > 1.0 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        elif dist > 3.0 and check_for_rotation == 1:
            rot = 0
            check_for_rotation = 2
        dist = dist + 0.14
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        time.sleep(0.5)


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
    client = Client("172.20.10.5", 5556)
    a_b_way(client)
