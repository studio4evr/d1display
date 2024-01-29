import subprocess
import os
import time
from PIL import Image

def hide_mouse_cursor():
    subprocess.run(['xdotool', 'mousemove', '0', '0'])

def send_key_event(key):
    subprocess.run(['xdotool', 'key', key])
    
def process_images(left_images, right_images, width, height, output_folder):
    combined_images = []
    for left_img, right_img in zip(left_images, right_images):
        image1 = Image.open(left_img)
        image2 = Image.open(right_img)
        combined_image = Image.new('RGB', (width, height))
        combined_image.paste(image1, (0, 0))
        combined_image.paste(image2, (image1.width, 0))
        combined_images.append(combined_image)

    os.makedirs(output_folder, exist_ok=True)

    for i, combined_image in enumerate(combined_images):
        output_path = os.path.join(output_folder, f'combined_{i + 1}.jpg')
        combined_image.save(output_path)

    return output_folder

def run_slideshow(client_number):
    left_folder = f'/home/d1/Slides/Screen00{client_number}/'
    right_folder = f'/home/d1/Slides/Screen00{client_number+1}/'

    WIDTH = 3840
    HEIGHT = 1080

    left_images = sorted([os.path.join(left_folder, file) for file in os.listdir(left_folder) if file.endswith(('.jpg', '.png'))])
    right_images = sorted([os.path.join(right_folder, file) for file in os.listdir(right_folder) if file.endswith(('.jpg', '.png'))])

    output_folder = process_images(left_images, right_images, WIDTH, HEIGHT, f'/home/d1/Slides/CombinedImages_{client_number}/')

    image_paths = ' '.join([os.path.join(output_folder, f'combined_{i + 1}.jpg') for i in range(len(left_images))])

    feh_command = f'feh --borderless --geometry 3840x1080+0+0 {image_paths}'

    hide_mouse_cursor()

    feh_process = subprocess.Popen(feh_command, shell=True)
    feh_process.wait()
    
    while True:
        time.sleep(2)
        send_key_event('Right')


    

if __name__ == "__main__":
    client_number = 1
    run_slideshow(client_number)

