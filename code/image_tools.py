from PIL import Image
import os
import numpy as np


class ImageResizer:
    def __init__(self, input_path):
        self.input_path = input_path

    def resize_image(self):
        # Load the image
        image = Image.open(self.input_path)
        # Get the dimensions of the original image
        original_width, original_height = image.size
        # Compute the dimensions of the resized image
        resized_width = int(original_width * 0.8)
        resized_height = int(original_height * 0.8)
        # Resize the image
        resized_image = image.resize((resized_width, resized_height))
        return resized_image

    def save_resized_image(self, output_path):
        resized_image = self.resize_image()
        # Convert the image to RGB mode if it's in RGBA mode
        if resized_image.mode == "RGBA":
            resized_image = resized_image.convert("RGB")
        # Save the resized image in JPEG format
        resized_image.save(output_path, "JPEG")

    def save_resized_image_same_location(self):
        # Get the base name of the input file
        base, _ = os.path.splitext(self.input_path)
        # Construct the output file path
        output_path = f"{base}_thumbnail.jpg"
        # Save the resized image
        self.save_resized_image(output_path)


# Usage within another program:
# resizer = ImageResizer('input.png')
# resizer.save_resized_image_same_location()


class ImageCropper:
    def __init__(self, input_path, square_size):
        self.input_path = input_path
        self.square_size = square_size

    def compute_brightness(self, image):
        data = np.array(image) / 255.0
        brightness = np.mean(
            0.299 * data[:, :, 0] + 0.587 * data[:, :, 1] + 0.114 * data[:, :, 2]
        )
        return brightness

    def find_brightest_square(self, image):
        width, height = image.size
        max_brightness = 0
        brightest_square = None
        print("Cropper working...")

        for x in range(width - self.square_size + 1):
            for y in range(height - self.square_size + 1):
                square = image.crop((x, y, x + self.square_size, y + self.square_size))
                brightness = self.compute_brightness(square)
                if brightness > max_brightness:
                    max_brightness = brightness
                    brightest_square = (x, y)

        return brightest_square

    def crop_brightest_square(self):
        image = Image.open(self.input_path)
        x, y = self.find_brightest_square(image)
        cropped_image = image.crop((x, y, x + self.square_size, y + self.square_size))
        return cropped_image

    def save_cropped_image(self, output_path):
        cropped_image = self.crop_brightest_square()
        cropped_image.save(output_path)

    def save_cropped_image_same_location(self):
        base, ext = os.path.splitext(self.input_path)
        output_path = f"{base}_square{ext}"
        self.save_cropped_image(output_path)


# Usage within another program:
# cropper = ImageCropper('input.png', 1080)
# cropper.save_cropped_image_same_location()
