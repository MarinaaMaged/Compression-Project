import heapq
import os
from collections import Counter


class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.root = None  # Initialize the root variable

    class Node:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def make_frequency_dict(self, text):
        return Counter(text)

    def build_heap(self, frequency):
        for key, freq in frequency.items():
            node = self.Node(key, freq)
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            # Remove two nodes with the smallest frequency
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            # Create a new node with the combined frequency
            merged = self.Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            # Add the merged node back to the heap
            heapq.heappush(self.heap, merged)



        # After merging, the heap should contain only one node, which is the root
        if self.heap:
            self.root = self.heap[0]  # Take the root (the only node remaining)

        else:
            self.root = None


    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:  # Only assign codes to leaf nodes
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
        else:
            # Internal node (no character), just skip it
            pass
        
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        if self.root is not None:
            self.make_codes_helper(self.root, "")
        else:
            raise ValueError("Root is None, cannot generate codes.")

    def get_encoded_text(self, text):
        encoded_text = []
        for char in text:
            if char not in self.codes:
                raise KeyError(f"Character '{char}' not found in Huffman codes.")
            encoded_text.append(self.codes[char])
        return "".join(encoded_text)

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = f"{extra_padding:08b}"
        return padded_info + encoded_text

    def serialize_tree(self, root):
        if root is None:
            return "0"  # Null node
        if root.char is not None:
            return f"1{root.char}"  # Leaf node
        return f"2{self.serialize_tree(root.left)}{self.serialize_tree(root.right)}"

    def compress(self, file_path):
        base_name = os.path.splitext(file_path)[0]
        output_path = f"{base_name}_compressed.bin"

        with open(file_path, 'r') as file:
            text = file.read()

        if not text.strip():
            raise ValueError("Input file is empty or contains only whitespace.")

        frequency = self.make_frequency_dict(text)
        self.build_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        serialized_tree = self.serialize_tree(self.root)

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        with open(output_path, 'wb') as output:
            tree_length = len(serialized_tree)
            output.write(tree_length.to_bytes(4, 'big'))
            output.write(serialized_tree.encode())

            byte_array = bytearray()
            for i in range(0, len(padded_encoded_text), 8):
                byte = padded_encoded_text[i:i + 8]
                byte_array.append(int(byte, 2))
            output.write(bytes(byte_array))

        return output_path

    def deserialize_tree(self, serialized_tree):
        if not serialized_tree:
            return None, serialized_tree

        node_type = serialized_tree[0]
        serialized_tree = serialized_tree[1:]

        if node_type == "0":  # Null node
            return None, serialized_tree
        elif node_type == "1":  # Leaf node
            char = serialized_tree[0]
            serialized_tree = serialized_tree[1:]
            return self.Node(char, 0), serialized_tree
        elif node_type == "2":  # Internal node
            left, serialized_tree = self.deserialize_tree(serialized_tree)
            right, serialized_tree = self.deserialize_tree(serialized_tree)
            node = self.Node(None, 0)
            node.left = left
            node.right = right
            return node, serialized_tree

    def decompress(self, file_path):
        base_name = os.path.splitext(file_path)[0]
        output_path = f"{base_name}_decompressed.txt"
        with open(file_path, 'rb') as file:
            tree_length = int.from_bytes(file.read(4), 'big')
            serialized_tree = file.read(tree_length).decode()

            root, _ = self.deserialize_tree(serialized_tree)
            self.make_codes_helper(root, "")

            bit_string = ""
            byte = file.read(1)
            while byte:
                bit_string += f"{ord(byte):08b}"
                byte = file.read(1)

        if not bit_string:
            raise ValueError("Compressed file is empty or corrupted.")

        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)
        bit_string = bit_string[8:-extra_padding]

        current_code = ""
        decoded_text = []
        for bit in bit_string:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text.append(self.reverse_mapping[current_code])
                current_code = ""

        with open(output_path, 'w') as output:
            output.write("".join(decoded_text))

        return output_path
