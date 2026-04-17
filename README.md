# Construction Content Generator

A specialized GenAI content generation tool tailored for construction professionals. Built using Python, Groq LLaMA API, ChromaDB, and ReportLab.

## Features

- Generate 6 types of professional construction reports
- Site Report, Safety Report, Progress Report, Inspection Report, Daily Report, Material Report
- Voice input support for topic entry
- PDF export for every report
- Vector DB memory for consistent tone and terminology
- Clean minimal web UI

## Tech Stack

- **Backend:** Python, Flask
- **LLM:** Groq API (LLaMA 3.3 70B)
- **Vector DB:** ChromaDB
- **PDF:** ReportLab
- **Frontend:** HTML, CSS, JavaScript

## Project Structure
```bash
construction-content-generator/
├── app/
│   ├── generator.py       # LLM generation logic
│   ├── vector_store.py    # ChromaDB vector storage
│   ├── prompts.py         # Prompt templates
│   └── pdf_exporter.py    # PDF generation
├── data/
│   └── exports/           # Generated PDF reports
├── index.html             # Frontend UI
├── api.py                 # Flask API server
├── main.py                # CLI entry point
├── requirements.txt
└── .env                   # API keys (not pushed to GitHub)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/construction-content-generator.git
cd construction-content-generator
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
Create a `.env` file in the root folder and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here

Get your free API key at: https://console.groq.com

### 5. Run the application
```bash
python api.py
```

### 6. Open in browser
http://127.0.0.1:5000

## Usage

1. Select a report type from the 6 options
2. Enter a construction topic (or click the 🎤 mic button to speak)
3. Enter the site location
4. Click **Generate Report**
5. View the formatted report on screen
6. Click **Download PDF** to save

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |

