import socket
import threading
import time
import subprocess
import os
from PIL import Image

# Global variable to store the assignment number
assignment_number = None

def hide_mouse_cursor():
    subprocess.run(['xdotool', 'mousemove', '0', '0'])

# Function to send a key event to feh using xdotool
def send_key_event(key):
    subprocess.run(['xdotool', 'key', key])
    
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

def send_ready_for_next_slide_message():
    # Send a message to the server indicating that the client is ready for the next slide
    global assignment_number
    if assignment_number is not None:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.1.0', 12346))  # Replace with the actual IP address and port
            client_socket.send("readyForNextSlide".encode('utf-8'))
            client_socket.close()
        except Exception as e:
            print(f"Error sending ready for next slide message: {e}")

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
    # Total size of local displays
    WIDTH = 3840
    HEIGHT = 1080

    left_images = sorted([os.path.join(left_folder, file) for file in os.listdir(left_folder) if file.endswith(('.jpg', '.png'))])
    right_images = sorted([os.path.join(right_folder, file) for file in os.listdir(right_folder) if file.endswith(('.jpg', '.png'))])

    # Check if combined folder exists
    combined_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}Combined/'
    if not os.path.exists(combined_folder):
        print("Combining images into folder:", combined_folder)
        combined_images = []
        for left_img, right_img in zip(left_images, right_images):
            image1 = Image.open(left_img)
            image2 = Image.open(right_img)
            combined_image = Image.new('RGB', (WIDTH, HEIGHT))
            combined_image.paste(image1, (0, 0))
            combined_image.paste(image2, (image1.width, 0))
            combined_images.append(combined_image)

        os.makedirs(combined_folder, exist_ok=True)

        for i, combined_image in enumerate(combined_images):
            output_path = os.path.join(combined_folder, f'combined_{i + 1}.jpg')
            combined_image.save(output_path)
    else:
        print("Combined folder already exists. Skipping image processing.")

    # Start slideshow
    output_paths = sorted([os.path.join(combined_folder, file) for file in os.listdir(combined_folder) if file.startswith('combined_')])
    image_paths = ' '.join(output_paths)
    feh_command = f'feh --borderless --geometry 3840x1080+0+0 {image_paths}'
    subprocess.Popen(feh_command, shell=True)
    send_ready_for_next_slide_message()

def next_slide_function():
    # Implement your logic for handling next slide command here
    print("Next slide command received from server. Implementing next slide functionality...")
    send_key_event('Right')

if __name__ == "__main__":
    run_client()
