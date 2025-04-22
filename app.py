from flask import Flask, request, jsonify
import pdfplumber
from io import BytesIO
import traceback

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
            for i, page in enumerate(pdf.pages):
                try:
                    texto += page.extract_text() or ""
                    for table in page.extract_tables():
                        tabelas.append(table)
                except Exception as page_error:
                    print(f"Erro ao processar página {i}: {page_error}")
                    continue  # Pula a página com erro

        return jsonify({
            'texto': texto,
            'tabelas': tabelas
        })

    except Exception as e:
        # Imprime o stack trace no log do Render (importante pra debug!)
        print("Erro geral ao processar PDF:")
        traceback.print_exc()
        return jsonify({'error': 'Erro interno ao processar PDF', 'details': str(e)}), 500
