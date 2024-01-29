import pigpio
import time

# Set the GPIO pin numbers for UART
tx_pin = 14  # GPIO 14 (TXD) - Transmit Pin

# Specify the Pigpio host/port
pi = pigpio.pi('localhost', 8888)

# Set up UART on the server side
serial_handle = pi.serial_open(tx_pin, 9600)

# Function to send a byte over UART
def send_byte(byte):
    pi.serial_write(serial_handle, chr(byte))

# Function to send a message over UART
def send_message(message):
    for char in message:
        send_byte(ord(char))
        time.sleep(0.1)  # Adjust timing as needed

# Example
try:
    message_to_send = "StartSlideshow"
    send_message(message_to_send)

finally:
    pi.serial_close(serial_handle)  # Close the serial connection on exit
    pi.stop()
