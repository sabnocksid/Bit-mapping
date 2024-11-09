from PIL import Image, ImageDraw, ImageFont
import os

# Path to save the images in the alphabet_images folder in the same directory as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'alphabet_images')
os.makedirs(output_dir, exist_ok=True)

# Font size and image size
font_size = 200
image_size = (250, 250)

# Load a font (you may need to specify a full path if not a default font)
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except IOError:
    font = ImageFont.load_default()

# Generate images for each letter from A to Z
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    # Create a new blank image
    img = Image.new('RGB', image_size, color='white')
    draw = ImageDraw.Draw(img)

    # Calculate the position to center the letter
    text_bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

    # Draw the letter on the image
    draw.text(position, letter, fill='black', font=font)

    # Save the image as a PNG file in the alphabet_images folder
    img.save(os.path.join(output_dir, f"{letter}.png"))

print("Alphabet PNG images created in:", output_dir)
