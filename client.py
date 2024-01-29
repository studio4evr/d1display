import socket
import threading

def send_message(client_socket):
    while True:
        message = input("Enter a message: ")
        client_socket.send(message.encode('utf-8'))

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.0', 12345))  # Replace with the actual IP address of Pi 1 and the chosen port

    print("[+] Connected to the server")

    message_sender = threading.Thread(target=send_message, args=(client,))
    message_sender.start()

    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    run_client()
