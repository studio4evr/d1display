import subprocess
import os
import time
from PIL import Image

# Function to get the list of image files in a directory
def get_image_files(directory):
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    return sorted(image_files, key=lambda x: int(''.join(filter(str.isdigit, x))))

# Directories for left and right images
left_directory = '/home/d1/Slides/Screen001'
right_directory = '/home/d1/Slides/Screen002'

# Get lists of image files for left and right directories
left_images = get_image_files(left_directory)
right_images = get_image_files(right_directory)

# Ensure both lists have the same length
min_length = min(len(left_images), len(right_images))
left_images = left_images[:min_length]
right_images = right_images[:min_length]

# Width and height of the combined image
WIDTH = 3840
HEIGHT = 1080

# Create a new image with the combined size
combined_image = Image.new('RGB', (WIDTH, HEIGHT))

# Control the duration each image is displayed (in seconds)
display_duration = 5  # Adjust this value as needed
feh_process = None

for left_image, right_image in zip(left_images, right_images):
    # Paths for left and right images
    left_path = os.path.join(left_directory, left_image)
    right_path = os.path.join(right_directory, right_image)
    left_image = Image.open(left_path)
    right_image = Image.open(right_path)
    
    # Paste the left and right images side by side
    combined_image.paste(left_image, (0, 0))
    combined_image.paste(right_image, (left_image.width, 0))
    
    # Save the combined image
    combined_image.save('combined_image.jpg')
    
    if feh_process is not None:
        # If the process is still running, terminate it
        feh_process.terminate()

    # Command to open feh in the background with the combined image
    command = [
        'feh',
        '--borderless',
        '--geometry', f'3840x1080+0+0',
        'combined_image.jpg'
    ]

    # Open feh in the background using subprocess.Popen
    feh_process = subprocess.Popen(command)

    # Wait for the specified duration before continuing to the next image
    time.sleep(display_duration)

    # Terminate the feh process to move on to the next iteration
    
# If there are multiple processes, wait for all to finish before exiting
feh_process.wait()
