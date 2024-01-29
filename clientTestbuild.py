import socket
import threading
import time

# Global variable to store the assignment number
assignment_number = None

def receive_assignment(client_socket):
    global assignment_number
    assignment = client_socket.recv(1024).decode('utf-8')
    print(f"You are assigned client number: {assignment}")
    assignment_number = assignment

def handle_server_commands(client_socket):
    while True:
        command = client_socket.recv(1024).decode('utf-8')
        if not command:
            break
        if command == "beginSlideShow" and assignment_number is not None:
            print("Attempting to begin slideshow...")
            folders = identify_folders(assignment_number)
            if folders is not None:
                left_folder, right_folder = folders
                start_slideshow(left_folder, right_folder)
            else:
                print("Invalid assignment number. Unable to identify folders.")
        elif command == "nextSlide":
            next_slide_function()  # Call your function here for handling next slide command
        else:
            print(f"Received from server: {command}")


def run_client():
    global assignment_number
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('192.168.1.0', 12346))  # Replace with the actual IP address and port

        print("[+] Connected to the server")

        # Receive the assignment number only once
        receive_assignment(client)

        # Listen for server commands in a separate thread
        command_listener = threading.Thread(target=handle_server_commands, args=(client,))
        command_listener.start()

        # Wait for the command listener thread to finish before closing the client
        command_listener.join()

    except ConnectionRefusedError:
        print("Connection refused. Retrying in 5 seconds...")
        time.sleep(5)

    finally:
        # Close the client socket
        client.close()

def convert_assignment_to_folders(assignment):
    if assignment == 1:
        return [1, 2]
    elif assignment == 2:
        return [3, 4]
    elif assignment == 3:
        return [5, 6]
    elif assignment == 4:
        return [7, 8]
    elif assignment == 5:
        return [9, 1]
    else:
        return None

def identify_folders(assignment):
    if assignment is not None:
        assignment_number = int(assignment)  # Ensure assignment is an integer
        folder_numbers = convert_assignment_to_folders(assignment_number)
        if folder_numbers:
            print("Assigning folders...")
            # Convert folder numbers to paths
            folder_paths = [f'/home/d1/Slides/Screen{str(folder).zfill(3)}/' for folder in folder_numbers]
            return folder_paths
    return None

def start_slideshow(left_folder, right_folder):
    # Implement logic to start the slideshow using the identified folders
    print("Starting slideshow with left folder:", left_folder)
    print("Starting slideshow with right folder:", right_folder)

def next_slide_function():
    # Implement your logic for handling next slide command here
    print("Next slide command received from server. Implementing next slide functionality...")

if __name__ == "__main__":
    run_client()
