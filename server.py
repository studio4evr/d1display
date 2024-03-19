import socket
import threading
import time
import pygame

# Use a global variable to track compiling state
is_compiling = False
compiling_lock = threading.Lock()
compiling_condition = threading.Condition(compiling_lock)

# Define the interim type mapping based on client IDs
interim_type_mapping = {
    1: "L03R08",
    2: "R00L05",
    3: "L02R12",
    4: "L03R09",
    5: "L06R08"
}

def handle_client(client_socket, client_id, clients):
    global is_compiling
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Received from client {client_id}: {message}")

        if message == "compiling":
            with compiling_condition:
                is_compiling = True
                print(f"Client {client_id} compiling. Waiting for completion.")
                compiling_condition.wait()  # Wait for compiling to finish
                print(f"Client {client_id} finished compiling. Continuing.")

        elif message == "compiling finished":
            with compiling_condition:
                is_compiling = False
                compiling_condition.notify_all()  # Notify all waiting threads

def send_message_to_all_clients(clients, message):
    global is_compiling
    if is_compiling:
        print("Waiting for compiling to finish before sending messages.")
        with compiling_condition:
            compiling_condition.wait_for(lambda: not is_compiling)

    for client_socket, _ in clients:
        try:
            client_socket.send(message.encode('utf-8'))
            print(f"Sent message: {message}")
        except Exception as e:
            print(f"Error occurred while sending message: {e}")

def assign_client_id(addr):
    ip_last_octet = addr[0].split('.')[-1]
    id_mapping = {
        '0': 1,
        '5': 2,
        '2': 3,
        '4': 4,
        '3': 5
    }
    return id_mapping.get(ip_last_octet, None)

def assign_and_notify_client(client_socket, addr, clients):
    client_id = assign_client_id(addr)
    if client_id is not None:
        interimType = interim_type_mapping.get(client_id, "L")  # Default to L if not found
        msg = str(client_id) + interimType
        client_socket.send(msg.encode('utf-8'))
        print(f"[+] Assigned ID:{client_id} to {addr} with interim {interimType}")

        # Add client to the list and handle further communication in a thread
        clients.append((client_socket, client_id))
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id, clients))
        client_handler.start()
    else:
        print("Invalid client IP address. Connection closed.")
        client_socket.close()

def init_sound():
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    mp3_file = '/home/d1/Slides/MID-MASTER-FILE_STEREO.mp3'
    # mp3_file = '/home/d1/Downloads/no-sweat-2.mp3'
    pygame.mixer.music.load(mp3_file)

    # Play the MP3 file, looped indefinitely
    pygame.mixer.music.play(-1)

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.0', 12346))
    server.listen(5)
    print("[+] Server listening for incoming connections")
    EXPECTED_CLIENTS = 5
    clients = []

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Accepted connection from {addr[0]}:{addr[1]}")

        # Assign client ID and notify the client of its interim image type
        assign_and_notify_client(client_socket, addr, clients)

        # Now wait for all expected clients to connect before proceeding
        if len(clients) == EXPECTED_CLIENTS :  # Assuming 5 is the number of expected clients
            print("[+] All clients connected. Configuring clients...")
            break

    time.sleep(5)  # Wait a bit before starting the slideshow

    # Starting the slideshow
    init_sound()
    send_message_to_all_clients(clients, "beginSlideShow")
    time.sleep(10)
    #send_message_to_all_clients(clients, "nextSlide")
    send_message_to_all_clients(clients, "extraSlide")
    slideNumber = 1
    while True:
		# Slideshow Speed:
        time.sleep(10)
        ##
        print(f"Showing slide {slideNumber}")
        send_message_to_all_clients(clients, "nextSlide")
        slideNumber = slideNumber + 1
        if slideNumber > 195:
            print("Restarting...")
            slideNumber = 1
            time.sleep(1)
            send_message_to_all_clients(clients, "extraSlide")
            

if __name__ == "__main__":
    run_server()
