from PIL import Image
import subprocess

# Load the two images
image1_path = '/home/d1/Slides/Screen001/001.jpg'
image2_path = '/home/d1/Slides/Screen001/002.jpg'

# Open the images using PIL
image1 = Image.open(image1_path)
image2 = Image.open(image2_path)

WIDTH = 3840
HEIGHT = 1080

# Create a new image with the combined size
combined_image = Image.new('RGB', (WIDTH, HEIGHT))

# Paste the images side by side
combined_image.paste(image1, (0, 0))
combined_image.paste(image2, (image1.width, 0))

# Save or display the combined image
# Save the combined image
combined_image.save('combined_image.jpg')

# Open the combined image using feh
subprocess.run(['feh', '--borderless', '--geometry', '3840x1080+0+0', 'combined_image.jpg'])
