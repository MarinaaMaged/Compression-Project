import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

class ImageQuantization:
    def __init__(self, image_path, num_levels=16):
        self.image_path = image_path
        self.num_levels = num_levels
        self.image = self.load_image()
        self.image_array = np.array(self.image)
        self.quantized_image = None
        self.decompressed_image = None
        self.step_size = None

    def load_image(self):
        """
        Load the image and handle invalid paths or formats.
        """
        try:
            
            if not os.path.isfile(self.image_path):
                raise FileNotFoundError("The provided image path does not exist.")
            
            valid_formats = ['.jpg', '.jpeg', '.png']
            if not any(self.image_path.lower().endswith(ext) for ext in valid_formats):
                raise ValueError("The image format is not supported. Please use JPEG, JPG, or PNG.")
            
            # Open the image
            image = Image.open(self.image_path)
            return image

        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading image: {e}")
            raise

    def uniform_quantization(self, output_path):
        """
        Perform uniform quantization on the image and save the quantized image.
        """
        image = np.asarray(self.image, dtype=np.float32)
        img_min, img_max = np.min(image), np.max(image)
        self.step_size = (img_max - img_min) / self.num_levels
        self.quantized_image = np.floor((image - img_min) / self.step_size) * self.step_size + img_min

        # Save the quantized image to the specified output path
        quantized_img = Image.fromarray(self.quantized_image.astype(np.uint8))
        quantized_img.save(output_path)
        print(f"Quantized image saved to {output_path}")
        return output_path

    def decompress_image(self, output_path):
        """
        Decompress the quantized image and save the decompressed image.
        """
        self.decompressed_image = self.quantized_image + (self.step_size / 2)
        decompressed_img = np.clip(self.decompressed_image, 0, 255).astype(np.uint8)

        # Save the decompressed image to the specified output path
        decompressed_img = Image.fromarray(decompressed_img)
        decompressed_img.save(output_path)
        print(f"Decompressed image saved to {output_path}")
        return output_path

    def calculate_mse(self):
        """
        Calculate the Mean Squared Error between the original and decompressed images.
        """
        return np.mean((self.image_array - self.decompressed_image) ** 2)

    def compression_rate(self):
        """
        Calculate the compression rate of the quantized image.
        """
        original_size = self.image_array.size * self.image_array.itemsize
        quantized_size = self.quantized_image.size * self.quantized_image.itemsize
        return original_size / quantized_size

    def display_images(self):
        """
        Display the original, quantized, and decompressed images.
        """
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.title("Original Image")
        plt.imshow(self.image_array, cmap="gray")
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.title("Quantized Image")
        quantized_display = np.clip(self.quantized_image, 0, 255).astype(np.uint8)
        plt.imshow(quantized_display, cmap="gray")
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.title("Dequantized Image")
        decompressed_display = np.clip(self.decompressed_image, 0, 255).astype(np.uint8)
        plt.imshow(decompressed_display, cmap="gray")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    def quanty (self):
        image_path = self.image_path

        compressed_path = "quantized_image.jpg"
        decompressed_path = "dequantized_image.jpg"

        
        num_levels = self.num_levels

        # instance of ImageQuantization
        quantizer = ImageQuantization(image_path, num_levels)

        compressed_file = quantizer.uniform_quantization(compressed_path)
        decompressed_file = quantizer.decompress_image(decompressed_path)
        return compressed_file , decompressed_file




if __name__ == "__main__":
    try:
        image_path = input("Enter the path to the image: ").strip()

        compressed_path = "quantized_image.png"
        decompressed_path = "dequantized_image.png"

        
        num_levels = int(input("Enter the number of quantization levels: "))

        # instance of ImageQuantization
        quantizer = ImageQuantization(image_path, num_levels)

        
        quantizer.uniform_quantization(compressed_path)
        quantizer.decompress_image(decompressed_path)

        mse = quantizer.calculate_mse()
        compression_rate = quantizer.compression_rate()

        print(f"Step Size: {quantizer.step_size}")
        print(f"Compression Rate: {compression_rate:.2f}")
        print(f"Mean Squared Error (MSE): {mse:.2f}")

        quantizer.display_images()

    except Exception as e:
        print(f"An error occurred: {e}") 
