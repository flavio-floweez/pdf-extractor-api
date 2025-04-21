from flask import Flask, request, jsonify
import pdfplumber
from io import BytesIO

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        pdf_file = BytesIO(file.read())
        texto = ""
        tabelas = []

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() or ""
                for table in page.extract_tables():
                    tabelas.append(table)

        return jsonify({
            'texto': texto,
            'tabelas': tabelas
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
