import sqlite3
import serial
import re

def initialize_serial(port="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0", baudrate=115200, timeout=3):
    """Initialize the serial connection."""
    try:
        ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        if (ser.isOpen()):
            ser.close()
            ser.open()
            print("Serial port open + initialized.")
    except serial.SerialException as e:
        print("Failed to initialize serial port:", e)
        exit(1)
    return ser

def update_database(data):
    """Inserts parsed data into the database."""
    conn = sqlite3.connect('serial_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO serial_data (samples)
        VALUES (?)
    ''', (data,))
    conn.commit()
    conn.close()
    print("Data inserted into database")

def parse_serial_data(line):
    """Parse received serial data and return relevant information."""
    # Extract audio samples from the line
    samples_match = re.findall(r'(-?\d+)', line)
    # Join the samples into a comma-separated string
    samples_str = ', '.join(samples_match)
    return samples_str

def read_from_serial(ser):
    """Read data from serial and process it."""
    try:
        while True:
            raw_line = ser.readline()
            if raw_line:
                line = raw_line.decode().strip()
                print(f"Raw line: {line}")
                parsed_data = parse_serial_data(line)
                print(f"parsed data: {parsed_data}")
                update_database(parsed_data)
            else:
                print("No more data.")
    except serial.SerialException as e:
        print("Error reading from serial port:", e)
    finally:
        ser.close()

def setup_database():
    conn = sqlite3.connect('serial_data.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS serial_data (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                samples TEXT
                )
    ''')
    conn.commit()
    conn.close()

def main():
    setup_database() 
    ser = initialize_serial()
    read_from_serial(ser)

if __name__ == "__main__":
    main()
