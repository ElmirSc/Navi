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
    while dist < 30.0:
        rot = 3
        if dist > 2.1 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        elif dist > 7.0 and check_for_rotation == 1:
            rot = 1
            check_for_rotation = 2
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        time.sleep(0.5)

def drive_c_d_way(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    while dist < 30.0:
        rot = 3
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        time.sleep(0.5)

def drive_a_b_way_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    while dist < 30.0:
        rot = 3
        if dist > 7.0 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        elif dist > 12.0 and check_for_rotation == 1:
            rot = 1
            check_for_rotation = 2
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        time.sleep(0.5)

def drive_c_d_way_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    while dist < 30.0:
        rot = 3
        if dist > 3.1 and check_for_rotation == 0:
            rot = 0
            check_for_rotation = 1
        elif dist > 7.7 and check_for_rotation == 1:
            rot = 1
            check_for_rotation = 2
        elif dist > 12.3 and check_for_rotation == 2:
            rot = 1
            check_for_rotation = 3
        elif dist > 17.0 and check_for_rotation == 3:
            rot = 0
            check_for_rotation = 4
        dist = dist + 0.1
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
    client = Client("192.168.0.8", 5556)
    drive_c_d_way_wrong(client)
