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
        #Generate cumulative probabilities for symbols.
        cumulative_prob = {}
        cumulative = Decimal(0.0)

        for char, prob in sorted(symbol_probs.items()):
            cumulative_prob[char] = (cumulative, cumulative + Decimal(prob))
            cumulative += Decimal(prob)

        return cumulative_prob

    @staticmethod
    def encode(text, symbol_probs):
        #Perform arithmetic encoding
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
        #Perform arithmetic decoding 
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
        #Compress the text using arithmetic encoding.
        symbol_probs = ArithmeticCoding.calculate_symbol_probs(self.text)
        encoded_value = ArithmeticCoding.encode(self.text, symbol_probs)
        return encoded_value, symbol_probs

    def decompress(self, encoded_value, symbol_probs):
        #Decompress the encoded value to reconstruct the original text.
        return ArithmeticCoding.decode(encoded_value, len(self.text), symbol_probs)

if __name__ == "__main__":
    file_path = input("Enter the path to the file: ").strip()
    compressor = FileCompressor(file_path)

    compressor.load_text()
    print(f"Text extracted from file: {compressor.text.strip()}")

    encoded_value, symbol_probs = compressor.compress()
    print(f"Compressed Value: {encoded_value}")

    decompressed_text = compressor.decompress(encoded_value, symbol_probs)
    print(f"Decompressed Text: {decompressed_text.strip()}")
