import os
import ast
import math
from collections import Counter

class LZWCompression:
    def __init__(self):
        self.ascii_dict = dict(map(lambda i: (chr(i), i), range(128)))
        self.reverse_ascii_dict = dict(map(lambda i: (i, chr(i)), range(128)))

    def read_file(self, file_path):
        """Reads the content of a file and returns it as a string."""
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None

    def write_file(self, file_path, content):
        """Writes the given content to a file."""
        with open(file_path, 'w') as file:
            file.write(content)

    def compress(self, file_path):
        data = self.read_file(file_path)
        if not data:
            return None, 0

        base_name = os.path.splitext(file_path)[0]
        output_path = f"{base_name}_compressed.lzw"

        # Initialize compression variables
        current_sequence = ""
        compressed = []
        next_code = 128

        # Compression process
        for char in data:
            new_sequence = current_sequence + char
            if new_sequence in self.ascii_dict:
                current_sequence = new_sequence
            else:
                compressed.append(self.ascii_dict[current_sequence])
                self.ascii_dict[new_sequence] = next_code
                next_code += 1
                current_sequence = char

        # Add the last sequence to the output
        if current_sequence:
            compressed.append(self.ascii_dict[current_sequence])

        # Save compressed data
        self.write_file(output_path, str(compressed))

        # Calculate compression ratio
        if compressed:
            bit_length = math.ceil(math.log2(max(compressed) + 1))
            compression_ratio = (len(data) * 8) / (len(compressed) * bit_length)
        else:
            compression_ratio = 0

        return output_path, compression_ratio

    def decompress(self, file_path):
        compressed_data = self.read_file(file_path)
        if not compressed_data:
            return None, 0

        base_name = os.path.splitext(file_path)[0]
        output_path = f"{base_name}_decompressed.txt"

        # Convert string representation back to list
        compressed_data = ast.literal_eval(compressed_data)

        # Initialize decompression variables
        decompressed_data = []
        current_code = compressed_data.pop(0)
        prev_string = self.reverse_ascii_dict[current_code]
        decompressed_data.append(prev_string)
        next_code = 128

        for code in compressed_data:
            if code in self.reverse_ascii_dict:
                current_string = self.reverse_ascii_dict[code]
            elif code == next_code:
                current_string = prev_string + prev_string[0]
            else:
                raise ValueError("Invalid compressed data.")

            decompressed_data.append(current_string)

            # Update dictionary
            self.reverse_ascii_dict[next_code] = prev_string + current_string[0]
            next_code += 1

            prev_string = current_string

        # Save decompressed data
        decompressed_text = ''.join(decompressed_data)
        self.write_file(output_path, decompressed_text)

        return output_path, len(decompressed_text)

    def calculate_entropy(self, data):
        freq = Counter(data)
        total_symbols = len(data)
        probabilities = [count / total_symbols for count in freq.values()]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy

    def calculate_metrics(self, original_path, compressed_path):
        original_data = self.read_file(original_path)
        compressed_data = self.read_file(compressed_path)
        if not original_data or not compressed_data:
            return {}

        compressed_data = ast.literal_eval(compressed_data)

        # Calculate metrics
        entropy = self.calculate_entropy(original_data)
        original_bits = len(original_data) * 8
        compressed_bits = len(compressed_data) * math.ceil(math.log2(max(compressed_data) + 1))
        savings = (1 - compressed_bits / original_bits) * 100
        avg_bits = compressed_bits / len(original_data) if len(original_data) else 0
        efficiency = (entropy / avg_bits) * 100 if avg_bits else 0

        return {
            'entropy': entropy,
            'compression_ratio': original_bits / compressed_bits if compressed_bits else 0,
            'savings': savings,
            'average_bits_per_symbol': avg_bits,
            'efficiency': efficiency
        }
