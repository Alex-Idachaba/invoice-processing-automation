from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    file = request.files['image']

    if file.filename.lower().endswith(".pdf"):
        pdf_bytes = file.read()
        pages = convert_from_bytes(
            pdf_bytes,
            poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
        )
        image = pages[0]
    else:
        image = Image.open(file)

    extracted_text = pytesseract.image_to_string(image)
    return jsonify({"text": extracted_text})

if __name__ == "__main__":
    app.run(port=5000)