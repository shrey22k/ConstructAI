from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from app.generator import ContentGenerator
from app.pdf_exporter import PDFExporter
from datetime import date
import os
import webbrowser

app = Flask(__name__, static_folder='.')
CORS(app)

generator = ContentGenerator()
pdf_exporter = PDFExporter()

REPORT_TYPES = {
    "site_report": "Site Report",
    "safety_report": "Safety Report",
    "progress_report": "Progress Report",
    "inspection_report": "Inspection Report",
    "daily_report": "Daily Report",
    "material_report": "Material Report",
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic")
    location = data.get("location")
    report_type = data.get("report_type")
    today = str(date.today())

    report = generator.generate(topic=topic, report_type=report_type, location=location, date=today)

    os.makedirs("data/exports", exist_ok=True)
    pdf_filename = f"data/exports/{report_type}_{topic[:20].replace(' ', '_')}_{today}.pdf"
    pdf_exporter.export(report=report, filename=pdf_filename, title=REPORT_TYPES[report_type], location=location, date=today)

    return jsonify({"report": report, "pdf": pdf_filename})

@app.route("/download-pdf")
def download_pdf():
    pdf_path = request.args.get("path")
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)