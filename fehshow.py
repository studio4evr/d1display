import subprocess
import os
import time
from PIL import Image

def hide_mouse_cursor():
    subprocess.run(['xdotool', 'mousemove', '5840', '2080'])
    
# Set the paths for the image folders
left_folder = '/home/d1/Slides/Screen001/'
right_folder = '/home/d1/Slides/Screen002/'

# Get a list of image files in the folders
left_images = sorted([os.path.join(left_folder, file) for file in os.listdir(left_folder) if file.endswith(('.jpg', '.png'))])
right_images = sorted([os.path.join(right_folder, file) for file in os.listdir(right_folder) if file.endswith(('.jpg', '.png'))])

WIDTH = 3840
HEIGHT = 1080

# Create a list to store combined images
combined_images = []

# Combine left and right images and append to the list
for left_img, right_img in zip(left_images, right_images):
    image1 = Image.open(left_img)
    image2 = Image.open(right_img)

    combined_image = Image.new('RGB', (WIDTH, HEIGHT))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (image1.width, 0))
    combined_images.append(combined_image)

# Create a directory to save the combined images
output_folder = '/home/d1/Slides/CombinedImages/'
os.makedirs(output_folder, exist_ok=True)

# Save combined images
for i, combined_image in enumerate(combined_images):
    output_path = os.path.join(output_folder, f'combined_{i + 1}.jpg')
    combined_image.save(output_path)

# Create a space-separated string of image paths
image_paths = ' '.join([os.path.join(output_folder, f'combined_{i + 1}.jpg') for i in range(len(combined_images))])

# Use feh to run a slideshow without automatic advancement
feh_command = f'feh --borderless --geometry 3840x1080+0+0 {image_paths}'

#hide mouse
hide_mouse_cursor()
	
# Run the feh command in a separate process

feh_process = subprocess.Popen(feh_command, shell=True)


# Function to send a key event to feh using xdotool
def send_key_event(key):
    subprocess.run(['xdotool', 'key', key])

# Example: Advance to the next image after 5 seconds
while True:
    time.sleep(2)
    send_key_event('Right')

    # Check if the Escape key is pressed
    if user_input.lower() == 'escape':
        break


# Wait for the feh process to complete
#feh_process.wait()

