import ast
import math
import os
from collections import Counter

def read_file(file_path):
    """Reads the content of a file and returns it as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def write_file(file_path, content):
    """Writes the given content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)

def calculate_entropy(data):
    freq = Counter(data)
    total_symbols = len(data)
    probabilities = [count / total_symbols for count in freq.values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def calculate_average_bits_per_symbol(data, compressed):
    if not data or not compressed:
        return 0
    total_bits = len(compressed) * math.ceil(math.log2(max(compressed) + 1))
    return total_bits / len(data)

def calculate_compression_savings(original_data, compressed_data):
    original_bits = len(original_data) * 8
    compressed_bits = len(compressed_data) * math.ceil(math.log2(max(compressed_data) + 1))
    savings = (1 - compressed_bits / original_bits) * 100
    return savings

def calculate_compression_efficiency(original_data, compressed_data):
    compressed_entropy = calculate_entropy(original_data)
    average_bits = calculate_average_bits_per_symbol(original_data, compressed_data)
    return (compressed_entropy / average_bits) * 100

def lzw_compression(file_path):
    """Compresses the content of a file using LZW algorithm."""
    data = read_file(file_path)
    if not data:
        return None, None  # Return None if there's no data to compress

    base_name = os.path.splitext(file_path)[0]
    output_path = f"{base_name}_compressed.txt"

    # Initialize ASCII dictionary
    ascii_dict = {chr(i): i for i in range(128)}
    current_sequence = ""
    compressed = []
    next_code = 128

    # Compression process
    for next_char in data:
        new_sequence = current_sequence + next_char
        if new_sequence in ascii_dict:
            current_sequence = new_sequence
        else:
            compressed.append(ascii_dict[current_sequence])
            ascii_dict[new_sequence] = next_code
            next_code += 1
            current_sequence = next_char

    # Add the last sequence to the output
    if current_sequence:
        compressed.append(ascii_dict[current_sequence])

    write_file(output_path, str(compressed))

    # Metrics calculations
    compression_ratio = len(data) * 8 / (len(compressed) * math.ceil(math.log2(max(compressed) + 1)))
    entropy = calculate_entropy(data)
    avg_bits = calculate_average_bits_per_symbol(data, compressed)
    savings = calculate_compression_savings(data, compressed)
    efficiency = calculate_compression_efficiency(data, compressed)

    metrics = {
        "compression_ratio": compression_ratio,
        "entropy": entropy,
        "average_bits_per_symbol": avg_bits,
        "compression_savings": savings,
        "compression_efficiency": efficiency
    }

    return output_path, metrics

def lzw_decompress(file_path):
    """Decompresses a file compressed with the LZW algorithm."""
    compressed_data = read_file(file_path)
    if not compressed_data:
        print("Error: No data to decompress.")
        return None, None

    base_name = os.path.splitext(file_path)[0]
    output_path = f"{base_name}_decompressed.txt"

    # Parse the compressed data
    if isinstance(compressed_data, str):
        compressed_data = ast.literal_eval(compressed_data)

    # Initialize ASCII dictionary
    ascii_dict = {i: chr(i) for i in range(128)}
    dict_size = 128

    # Decompression variables
    current_code = compressed_data.pop(0)
    pre_string = ascii_dict[current_code]
    decompressed_data = [pre_string]

    for code in compressed_data:
        if code in ascii_dict:
            current = ascii_dict[code]
        elif code == dict_size:
            current = pre_string + pre_string[0]
        else:
            raise ValueError("Invalid compressed data.")

        decompressed_data.append(current)
        ascii_dict[dict_size] = pre_string + current[0]
        dict_size += 1
        pre_string = current

    decompressed_text = "".join(decompressed_data)
    write_file(output_path, decompressed_text)

    # Metrics calculations
    original_entropy = calculate_entropy(decompressed_text)
    metrics = {
        "entropy": original_entropy,
        "decompressed_length": len(decompressed_text)
    }

    return output_path, metrics

