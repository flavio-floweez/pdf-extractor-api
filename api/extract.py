import json
import pdfplumber
from io import BytesIO

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Only POST allowed"})
        }

    try:
        file = request.files["file"]
        pdf_file = BytesIO(file.read())
        texto = ""
        tabelas = []

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() or ""
                for table in page.extract_tables():
                    tabelas.append(table)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "texto": texto,
                "tabelas": tabelas
            }),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
