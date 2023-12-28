import socket

if __name__ == "__main__":
    HOST = '172.20.10.5'  # IP-Adresse deines Computers
    PORT = 5555  # Port, der für die Kommunikation verwendet wird

    # Socket erstellen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Socket an Adresse und Port binden
        server_socket.listen()  # Socket in den Empfangsmodus versetzen
        print(f"Server wartet auf Verbindung auf {HOST}:{PORT}")

        conn, addr = server_socket.accept()  # Verbindung akzeptieren
        print(f"Verbunden mit {addr}")

        while True:
            data = conn.recv(1024)  # Daten vom Raspberry Pi empfangen
            if not data:
                break
            print(f"Empfangene Daten: {data.decode()}")

        conn.close()  # Verbindung schließen