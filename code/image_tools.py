from PIL import Image
import os
import io
import numpy as np


# Most common operation
class ImageTools:
    def __init__(self, input_path, square_size, max_mb):
        self.input_path = input_path
        self.square_size = square_size
        self.max_mb = max_mb
        self.cropper = ImageCropper(input_path, square_size)
        self.resizer = ImageResizer(input_path, max_mb)

    def make_square_and_thumbnail(self):
        self.cropper.save_cropped_image_same_location()
        self.resizer.save_resized_image_same_location()


# Crops images to a square of the brightest region
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


# Resizes image based on user specified max size in mb
class ImageResizer:
    def __init__(self, input_path, max_mb):
        self.input_path = input_path
        self.max_mb = max_mb  # Max YouTube thumbnail size is 2mb

    def resize_image(self, scale_factor):
        image = Image.open(self.input_path)
        resized_width = int(image.width * scale_factor)
        resized_height = int(image.height * scale_factor)
        resized_image = image.resize((resized_width, resized_height))
        return resized_image

    def save_resized_image(self, output_path):
        scale_factor = 1.0
        print("Thumbnail resizer working...")
        while True:
            resized_image = self.resize_image(scale_factor)

            with io.BytesIO() as buffer:
                resized_image.save(buffer, "PNG")
                size_in_mb = len(buffer.getvalue()) / (1024 * 1024)
                if size_in_mb <= self.max_mb:
                    with open(output_path, "wb") as f:
                        f.write(buffer.getvalue())
                    break

            scale_factor *= 0.98  # This is super inneficient lol

    def save_resized_image_same_location(self):
        base, _ = os.path.splitext(self.input_path)
        output_path = f"{base}_thumbnail.png"
        self.save_resized_image(output_path)

    # Example usage
    # resizer = ImageResizer("path/to/image.jpg", 2)
    # resizer.save_resized_image_same_location()
