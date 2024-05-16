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
    client.connected_client.settimeout(0.5)
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
        client.receive_message()
        #time.sleep(0.5)

def drive_c_f_way(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 30.0:
        rot = 3
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_a_b_way_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
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
        #time.sleep(0.5)
        client.receive_message()

def drive_a_l_way(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 30.0:
        rot = 3
        if dist > 7.0 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        elif dist > 12.0 and check_for_rotation == 1:
            rot = 0
            check_for_rotation = 2
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_a_l_way_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 40.0:
        rot = 3
        if dist > 7.0 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        elif dist > 12.0 and check_for_rotation == 1:
            rot = 1
            check_for_rotation = 3
        elif dist > 16.3 and check_for_rotation == 3:
            rot = 1
            check_for_rotation = 4
        elif dist > 20.9 and check_for_rotation == 4:
            rot = 1
            check_for_rotation = 5
        elif dist > 25.5 and check_for_rotation == 5:
            rot = 1
            check_for_rotation = 6
        elif dist > 30.1 and check_for_rotation == 6:
            rot = 0
            check_for_rotation = 9
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_c_f_way_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
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
        #time.sleep(0.5)
        client.receive_message()


def drive_c_j_way(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 30.0:
        rot = 3
        if dist > 3.1 and check_for_rotation == 0:
            rot = 0
            check_for_rotation = 1
        elif dist > 7.7 and check_for_rotation == 1:
            rot = 1
            check_for_rotation = 2
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_c_j_way_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 50.0:
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
            rot = 1
            check_for_rotation = 4
        elif dist > 21.6 and check_for_rotation == 4:
            rot = 1
            check_for_rotation = 5
        elif dist > 26.2 and check_for_rotation == 5:
            rot = 1
            check_for_rotation = 6
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_k_j(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 50.0:
        rot = 3
        if dist > 3.1 and check_for_rotation == 0:
            rot = 0
            check_for_rotation = 1
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_k_j_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 50.0:
        rot = 3
        if dist > 8.1 and check_for_rotation == 0:
            rot = 0
            check_for_rotation = 1
        elif dist > 12.7 and check_for_rotation == 1:
            rot = 0
            check_for_rotation = 2
        elif dist > 17.2 and check_for_rotation == 2:
            rot = 1
            check_for_rotation = 3
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_g_k(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 50.0:
        rot = 3
        if dist > 2.1 and check_for_rotation == 0:
            rot = 0
            check_for_rotation = 1
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_g_k_wrong(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 50.0:
        rot = 3
        if dist > 2.1 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        elif dist > 6.7 and check_for_rotation == 1:
            rot = 0
            check_for_rotation = 2
        elif dist > 11.3 and check_for_rotation == 2:
            rot = 0
            check_for_rotation = 3
        elif dist > 15.9 and check_for_rotation == 3:
            rot = 0
            check_for_rotation = 4
        elif dist > 20.5 and check_for_rotation == 4:
            rot = 1
            check_for_rotation = 5
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

def drive_g_k_wrong_(client):
    counter = 1
    speed = 1
    dist = 0.0
    if not client.is_connected:
        client.connect_to_socket()
    check_for_rotation = 0
    client.receive_message()
    print(client.data)
    client.connected_client.settimeout(0.5)
    while dist < 50.0:
        rot = 3
        if dist > 2.1 and check_for_rotation == 0:
            rot = 1
            check_for_rotation = 1
        # elif dist > 6.7 and check_for_rotation == 1:
        #     rot = 0
        #     check_for_rotation = 2
        # elif dist > 11.3 and check_for_rotation == 2:
        #     rot = 0
        #     check_for_rotation = 3
        # elif dist > 15.9 and check_for_rotation == 3:
        #     rot = 0
        #     check_for_rotation = 4
        # elif dist > 20.5 and check_for_rotation == 4:
        #     rot = 1
        #     check_for_rotation = 5
        dist = dist + 0.1
        message = str(speed) + " " + str(dist) + " " + str(rot)
        print(dist)
        client.send_message(message)
        #time.sleep(0.5)
        client.receive_message()

if __name__ == "__main__":
    # testing socket connection
    client = Client("192.168.0.12", 5556)
    drive_c_j_way_wrong(client)
