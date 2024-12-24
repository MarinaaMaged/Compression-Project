from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import os
from werkzeug.utils import secure_filename
from Website.compression.huffmanCoding import HuffmanCoding
from Website.compression.lzw import lzw_compression,lzw_decompress


main = Blueprint('main', __name__)

# check allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Home route
@main.route('/')
def home():
    return render_template('index.html')

@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/huffman')
def huffman():
    return render_template('huffman.html')


@main.route('/lzw')
def lzw():
    return render_template('lzw.html')

@main.route('/vector')
def vector():
    return render_template('vector.html')


@main.route('/uniform')
def uniform():
    return render_template('uniform.html')


@main.route('/huffmanProcess', methods=['POST'])
def huffman_process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            action = request.form.get('action')
            huffman = HuffmanCoding()

            if action == 'compress':
                compressed_file = huffman.compress(filepath)
                return send_file(compressed_file, as_attachment=True, download_name=os.path.basename(compressed_file))
            elif action == 'decompress':
                decompressed_file = huffman.decompress(filepath)
                return send_file(decompressed_file, as_attachment=True, download_name=os.path.basename(decompressed_file))
            else:
                return jsonify({'error': 'Invalid action'}), 400
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return jsonify({'error': 'Invalid file type'}), 400


@main.route('/lzwProcess', methods=['POST'])
def lzw_process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            action = request.form.get('action')

            if action == 'compress':
                compressed_file,_ = lzw_compression(filepath)
                return send_file(compressed_file, as_attachment=True, download_name=os.path.basename(compressed_file))
            elif action == 'decompress':
                decompressed_file,_ = lzw_decompress(filepath)
                return send_file(decompressed_file, as_attachment=True, download_name=os.path.basename(decompressed_file))
            else:
                return jsonify({'error': 'Invalid action'}), 400
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return jsonify({'error': 'Invalid file type'}), 400
