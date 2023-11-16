from PIL import Image
import os
import io
import numpy as np


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


class ImageResizer:
    def __init__(self, input_path):
        self.input_path = input_path

    def resize_image(self, scale_factor):
        image = Image.open(self.input_path)
        resized_width = int(image.width * scale_factor)
        resized_height = int(image.height * scale_factor)
        resized_image = image.resize((resized_width, resized_height))
        return resized_image

    def save_resized_image(self, output_path, max_size_in_mb=2):
        scale_factor = 1.0
        print("Thumbnail resizer working...")
        while True:
            resized_image = self.resize_image(scale_factor)

            with io.BytesIO() as buffer:
                resized_image.save(buffer, "PNG")
                size_in_mb = len(buffer.getvalue()) / (1024 * 1024)
                if size_in_mb <= max_size_in_mb:
                    with open(output_path, "wb") as f:
                        f.write(buffer.getvalue())
                    break

            scale_factor *= 0.98  # Reduce size by 2% and try again

    def save_resized_image_same_location(self):
        base, _ = os.path.splitext(self.input_path)
        output_path = f"{base}_thumbnail.png"
        self.save_resized_image(output_path)


# Example usage
# resizer = ImageResizer("path/to/image.jpg")
# resizer.save_resized_image_same_location()
