import socket
import threading
import time
import subprocess
import os
from PIL import Image

# Global variables
assignment_number = None
firstTimeCode = None
secondTimeCode = None
client_socket = None  # Global variable to hold the client socket
interim_type = None  # Global variable to hold the type of interim image to use

def hide_mouse_cursor():
    subprocess.run(['xdotool', 'mousemove', '0', '0'])

def send_key_event(key):
    subprocess.run(['xdotool', 'key', key])

def receive_assignment(client_socket):
    global assignment_number, firstTimeCode, secondTimeCode
    assignmentReceive = client_socket.recv(1024).decode('utf-8')
    print(f"received {assignmentReceive}")
    assignment = assignmentReceive[0]
    interim_type = assignmentReceive[1]
    firstTimeCode = extract_numbers(assignmentReceive, 2,3)
    secondTimeCode = extract_numbers(assignmentReceive, 5,6)
    print(f"You are assigned client number: {assignment} and interim {interim_type} with timecodes {firstTimeCode} and {secondTimeCode}")
    assignment_number = assignment

def extract_numbers(string, digit1, digit2):
    if len(string) < digit2+1:
        print("Input string is too short.")
        return None
    else:
        second_char = string[digit1]
        third_char = string[digit2]
        if second_char.isdigit() and third_char.isdigit():
            combined_number = int(second_char + third_char)
            return combined_number
        else:
            print("Second and third characters must be numbers.")
            return None
            
def handle_server_commands():
    global client_socket, interim_type  # Declare use of the global variable
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
            next_slide_function()
        else:
            print(f"Received from server: {command}")

def send_message(message_to_server):
    global assignment_number
    if assignment_number is not None:
        try:
            client_socket.send(message_to_server.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
                  

def run_client():
    global assignment_number, client_socket
    connected = False
    while not connected:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.1.0', 12346))  # Replace with the actual IP address and port
            connected = True  # Connection successful
            print("[+] Connected to the server")

            # Receive the assignment number only once
            receive_assignment(client_socket)

            # Listen for server commands in a separate thread
            command_listener = threading.Thread(target=handle_server_commands)
            command_listener.start()

            # Wait for the command listener thread to finish before closing the client
            command_listener.join()

        except ConnectionRefusedError:
            print("Connection refused. Retrying in 5 seconds...")
            time.sleep(5)
        finally:
            if not connected:
                client_socket.close()  # Close the client socket if not connected

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
        return [9, 1]  # 10th Screen is a duplicate of first screen
    else:
        return None

def identify_folders(assignment):
    if assignment is not None:
        assignment_number = int(assignment)  # Ensure assignment is an integer
        folder_numbers = convert_assignment_to_folders(assignment_number)
        if folder_numbers:
            print("Assigning folders...")
            folder_paths = [f'/home/d1/Slides/Screen{str(folder).zfill(3)}/' for folder in folder_numbers]
            return folder_paths
    return None

def start_slideshow(left_folder, right_folder):
    global interim_type  # Use the global variable to determine which interim images to include
    WIDTH = 3840
    HEIGHT = 1080

    left_images = sorted([os.path.join(left_folder, file) for file in os.listdir(left_folder) if file.endswith(('.jpg', '.png'))])
    right_images = sorted([os.path.join(right_folder, file) for file in os.listdir(right_folder) if file.endswith(('.jpg', '.png'))])

    combined_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}Combined/'
    interimL_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}InterimL/'
    interimR_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}InterimR/'
    special_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}Special/'
    
    if not os.path.exists(combined_folder):
        send_message("compiling")
        print("Combining images into folder:", combined_folder)
        os.makedirs(combined_folder, exist_ok=True)

        interimL_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}InterimL/'
        interimR_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}InterimR/'
        os.makedirs(interimL_folder, exist_ok=True)
        os.makedirs(interimR_folder, exist_ok=True)

        special_folder = f'/home/d1/Slides/Client{assignment_number.zfill(2)}Special/'
        os.makedirs(special_folder, exist_ok=True)

        black_image = Image.new('RGB', (WIDTH, HEIGHT), "black")
        black_image_path = os.path.join(special_folder, 'black.jpg')
        black_image.save(black_image_path)

        if left_images:
            first_left_img_path = left_images[0]
            first_left_img = Image.open(first_left_img_path)
            left_and_black_image = Image.new('RGB', (WIDTH, HEIGHT))
            left_and_black_image.paste(first_left_img, (0, 0))
            left_and_black_image_path = os.path.join(special_folder, 'left_black.jpg')
            left_and_black_image.save(left_and_black_image_path)

        for i in range(len(left_images) - 1):
            left_img = left_images[i]
            right_img = right_images[i]
            print("Combining " + left_img + " & " + right_img + " in memory...")
            image1 = Image.open(left_img)
            image2 = Image.open(right_img)
            combined_image = Image.new('RGB', (WIDTH, HEIGHT))
            combined_image.paste(image1, (0, 0))
            combined_image.paste(image2, (image1.width, 0))
            output_path = os.path.join(combined_folder, f'combined_{i + 1:03}.jpg')
            combined_image.save(output_path)

            next_left_img = Image.open(left_images[i + 1])
            next_right_img = Image.open(right_images[i + 1])

            interimL_image = Image.new('RGB', (WIDTH, HEIGHT))
            interimL_image.paste(next_left_img, (0, 0))
            interimL_image.paste(image2, (next_left_img.width, 0))
            interimL_path = os.path.join(interimL_folder, f'interimL_{i + 1:03}.jpg')
            interimL_image.save(interimL_path)

            interimR_image = Image.new('RGB', (WIDTH, HEIGHT))
            interimR_image.paste(image1, (0, 0))
            interimR_image.paste(next_right_img, (image1.width, 0))
            interimR_path = os.path.join(interimR_folder, f'interimR_{i + 1:03}.jpg')
            interimR_image.save(interimR_path)
    else:
        print("Combined folder already exists. Skipping image processing.")
        
    print("Sorting Images based on show program...")

    special_images = [os.path.join(special_folder, 'black.jpg'), os.path.join(special_folder, 'left_black.jpg')]
    combined_images = sorted([os.path.join(combined_folder, file) for file in os.listdir(combined_folder) if file.startswith('combined_')])
    interim_images_folder = interimL_folder if interim_type == "L" else interimR_folder
    interim_images = sorted([os.path.join(interim_images_folder, file) for file in os.listdir(interim_images_folder)])
    
    image_sequence = special_images + combined_images[:1]  # Start with special images and the first combined image
    
    for combined_image, interim_image in zip(combined_images[1:], interim_images):
        image_sequence.extend([interim_image, combined_image])
        
    print("Sorting complete.")
    send_message("compiling finished")
	
    image_paths = ' '.join(image_sequence)
    feh_command = f'feh --borderless --geometry 3840x1080+0+0 --slideshow-delay 5 {image_paths}'
    #subprocess.Popen(feh_command, shell=True)
    print("showing first slide")
    waitfor(int(assignment_number) * 0.04)
    send_key_event('Right')
    send_message("Ready for next slide")

def waitfor(waittime):
    time.sleep(waittime)
    print(f"waiting for {waittime}")

def next_slide_function():
	
    print("Next slide command received from server. Implementing next slide functionality...")
    waitfor(int(firstTimeCode) * 0.04)
    #send_key_event('Right')
    waitfor((int(secondTimeCode) - int(firstTimeCode)) * 0.04)
    #send_key_event('Right')
    send_message("Ready for next slide")

if __name__ == "__main__":
    run_client()
