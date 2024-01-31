import socket
import threading
import time

def handle_client(client_socket, client_id):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received from client {client_id}: {data.decode('utf-8')}")

def send_message_to_all_clients(clients, message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode('utf-8'))
            print(f"Sent to {client_socket.getpeername()}: {message}")
        except Exception as e:
            print(f"Error occurred while sending message to {client_socket.getpeername()}: {e}")

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12346))  # Choose a port (e.g., 12345)
    server.listen(5)

    print("[+] Server listening for incoming connections")

    clients = []
    client_count = 0
    EXPECTED_CLIENTS = 5

    while client_count < EXPECTED_CLIENTS:
        client, addr = server.accept()
        print(f"[+] Accepted connection from {addr[0]}:{addr[1]}")

        client_count += 1
        clients.append(client)

        # Send client its assigned ID
        client.send(str(client_count).encode('utf-8'))

        client_handler = threading.Thread(target=handle_client, args=(client, client_count))
        client_handler.start()

    print("[+] All clients connected. Sending message to all clients...")

    time.sleep(5)

    # Send "beginSlideShow" message to each client individually
    for client_socket in clients:
        client_socket.send("beginSlideShow".encode('utf-8'))

    # Loop to send "nextSlide" message every 5 seconds
    while True:
        time.sleep(5)
        for client_socket in clients:
            client_socket.send("nextSlide".encode('utf-8'))



if __name__ == "__main__":
    run_server()
