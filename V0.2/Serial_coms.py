import serial
import time

packet_in_size = 0

coms = serial.Serial('COM6', 115200)
packet = {}


def stablish_coms(port, baudrate, packet_out_size):
    global coms
    global packet_in_size
    coms.close()
    coms = serial.Serial(port, baudrate)
    time.sleep(0.5)
    coms.write(packet_out_size)
    time.sleep(0.2)
    packet_in_size = coms.readline()


def send_packet(data):
    coms.write(data)


def receive_packet():
    global packet
    while True:
        try:
            packet = coms.readline().decode('utf-8', errors='ignore').strip()
            print(f"Data from Arduino: {data}")
        except UnicodeDecodeError as e:
            print(f"Error decoding data: {e}")
        break


coms.close()
# Define the serial port and baud rate
ser = serial.Serial('COM6', 115200)  # Replace 'COMX' with your actual serial port


try:
    while True:
        try:
            # Read data from Arduino
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Data from Arduino: {data}")
        except UnicodeDecodeError as e:
            print(f"Error decoding data: {e}")

        # Send data to Arduino
        message = input("Enter message to send to Arduino: ")
        ser.write(message.encode())

except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
