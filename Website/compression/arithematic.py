import os
from decimal import Decimal, getcontext
from PyPDF2 import PdfReader
from docx import Document

# Set high precision for arithmetic calculations
getcontext().prec = 50

class ArithmeticCoding:
    @staticmethod
    def calculate_symbol_probs(text):
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1

        total = len(text)
        probabilities = {char: freq / total for char, freq in frequency.items()}
        return probabilities

    @staticmethod
    def get_cumulative_prob(symbol_probs):
        cumulative_prob = {}
        cumulative = Decimal(0.0)

        for char, prob in sorted(symbol_probs.items()):
            cumulative_prob[char] = (cumulative, cumulative + Decimal(prob))
            cumulative += Decimal(prob)

        return cumulative_prob

    @staticmethod
    def encode(text, symbol_probs):
        low = Decimal(0.0)
        high = Decimal(1.0)
        cumulative_prob = ArithmeticCoding.get_cumulative_prob(symbol_probs)

        for char in text:
            range_ = high - low
            high = low + range_ * cumulative_prob[char][1]
            low = low + range_ * cumulative_prob[char][0]

        return (low + high) / 2

    @staticmethod
    def decode(encoded_value, length, symbol_probs):
        cumulative_prob = ArithmeticCoding.get_cumulative_prob(symbol_probs)
        decoded_text = ""

        for _ in range(length):
            for char, (low, high) in cumulative_prob.items():
                if low <= encoded_value < high:
                    decoded_text += char
                    encoded_value = (encoded_value - low) / (high - low)
                    break

        return decoded_text

class TextExtractor:
    @staticmethod
    def extract_text_from_pdf(file_path):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    @staticmethod
    def extract_text_from_docx(file_path):
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    @staticmethod
    def extract_text_from_txt(file_path):
        with open(file_path, "r") as f:
            return f.read()

class FileCompressor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""

    def load_text(self):
        file_ext = os.path.splitext(self.file_path)[1].lower()
        if file_ext == ".pdf":
            self.text = TextExtractor.extract_text_from_pdf(self.file_path)
        elif file_ext == ".docx":
            self.text = TextExtractor.extract_text_from_docx(self.file_path)
        else:
            self.text = TextExtractor.extract_text_from_txt(self.file_path)

    def compress(self):
        symbol_probs = ArithmeticCoding.calculate_symbol_probs(self.text)
        encoded_value = ArithmeticCoding.encode(self.text, symbol_probs)
        compressed_filename = "compressed_output.txt"
        with open(compressed_filename, 'w') as f:
            f.write(str(encoded_value))
        
        return compressed_filename

    def decompress(self):
        symbol_probs = ArithmeticCoding.calculate_symbol_probs(self.text)
        compressed_filename = "compressed_output.txt"
        
        with open(compressed_filename, 'r') as f:
            encoded_value_str = f.read().strip()
        
        encoded_value = Decimal(encoded_value_str)
        decompressed_text = ArithmeticCoding.decode(encoded_value, len(self.text), symbol_probs)
        
        decompressed_filename = "decompressed_output.txt"
        
        with open(decompressed_filename, 'w') as f:
            f.write(decompressed_text.strip())
        
        return decompressed_filename
    
    def comde(self):
        file_path = self.file_path
        compressor = FileCompressor(file_path)

        compressor.load_text()

        compressed_file_path = compressor.compress()
        decompressed_file_path = compressor.decompress()
        return compressed_file_path,decompressed_file_path



if __name__ == "__main__":
    file_path = input("Enter the path to the file: ").strip()
    compressor = FileCompressor(file_path)

    compressor.load_text()
    print(f"Text extracted from file: {compressor.text.strip()}")

    compressed_file_path = compressor.compress()
    print(f"Compressed Value saved to: {compressed_file_path}")

    decompressed_file_path = compressor.decompress()
    print(f"Decompressed Text saved to: {decompressed_file_path}")


