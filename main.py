from app.generator import ContentGenerator
from app.pdf_exporter import PDFExporter
from datetime import date
import os

REPORT_TYPES = {
    "1": ("site_report", "Site Report"),
    "2": ("safety_report", "Safety Report"),
    "3": ("progress_report", "Progress Report"),
    "4": ("inspection_report", "Inspection Report"),
    "5": ("daily_report", "Daily Report"),
    "6": ("material_report", "Material Report"),
}

def main():
    generator = ContentGenerator()
    pdf_exporter = PDFExporter()

    print("=== Construction Content Generator ===\n")

    print("Select Report Type:")
    for key, (_, label) in REPORT_TYPES.items():
        print(f"  {key}. {label}")

    choice = input("\nEnter choice (1-6): ").strip()

    if choice not in REPORT_TYPES:
        print(" Invalid choice. Defaulting to Site Report.")
        choice = "1"

    report_type, report_label = REPORT_TYPES[choice]

    topic = input(f"\nEnter topic for {report_label} (e.g., 'foundation inspection'): ")
    location = input("Enter site location: ")
    today = str(date.today())

    print(f"\n Generating {report_label}...\n")
    report = generator.generate(topic=topic, report_type=report_type, location=location, date=today)

    print("=" * 60)
    print(report)
    print("=" * 60)

    # Save as PDF
    os.makedirs("data/exports", exist_ok=True)
    pdf_filename = f"data/exports/{report_type}_{topic[:20].replace(' ', '_')}_{today}.pdf"
    pdf_exporter.export(
        report=report,
        filename=pdf_filename,
        title=report_label,
        location=location,
        date=today
    )
    print(f"\n {report_label} saved as PDF: {pdf_filename}")

if __name__ == "__main__":
    main()