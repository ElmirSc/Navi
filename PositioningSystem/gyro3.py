import smbus
import time

ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

# Initialisierung des SMBus
bus = smbus.SMBus(1)


def read_word(reg):
    high = bus.read_byte_data(0x68, reg)
    low = bus.read_byte_data(0x68, reg + 1)
    value = (high << 8) + low
    return value


def read_acceleration_data():
    # Beschleunigungsdaten auslesen
    accel_x = read_word(ACCEL_XOUT_H)
    accel_y = read_word(ACCEL_YOUT_H)
    accel_z = read_word(ACCEL_ZOUT_H)

    # Umrechnung in 16-Bit-Vorzeichenformat
    if accel_x > 32767:
        accel_x -= 65536
    if accel_y > 32767:
        accel_y -= 65536
    if accel_z > 32767:
        accel_z -= 65536

    return accel_x, accel_y, accel_z


try:
    initial_time = time.time()  # Startzeit fuer Zeitmessung
    initial_velocity_x = 0  # Anfangsgeschwindigkeit für x-Achse

    while True:
        # Beschleunigungsdaten abrufen
        accel_data = read_acceleration_data()
        accel_x, _, _ = accel_data  # Hier verwenden wir nur die Beschleunigung in der x-Achse

        # Umrechnung von G-Kraeften in m/s^2 (bei Bedarf anpassen)
        acceleration_x = 9.81 * accel_x

        # Zeitmessung
        current_time = time.time()
        time_elapsed = current_time - initial_time

        # Geschwindigkeitsschaetzung durch Integration der Beschleunigung über die Zeit
        velocity_x = initial_velocity_x + acceleration_x * time_elapsed

        # Anzeigen der geschaetzten Geschwindigkeit
        print("Geschwindigkeit in Metern pro Sekunde (X-Achse):", velocity_x)

        # Aktualisierung der Anfangsgeschwindigkeit und Zeit für den naechsten Schleifendurchlauf
        initial_velocity_x = velocity_x
        initial_time = current_time

        time.sleep(0.1)  # Kurze Pause vor der naechsten Messung

except KeyboardInterrupt:
    pass

finally:
    bus.close()
