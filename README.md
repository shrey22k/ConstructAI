# ConstructAI — Construction Content Generator

A specialized **Generative AI** application built for construction professionals. It transforms basic construction topics into professional, industry-standard reports using advanced Prompt Engineering, a Vector Database for context retrieval, and a multi-step **Planner Agent** powered by LangChain and Groq API.

---

## Problem Statement

Construction professionals spend significant time manually drafting complex documentation such as Site Reports, Safety Reports, and Progress Reports. **ConstructAI** reduces this effort drastically by generating high-quality, consistent, and industry-standard reports in seconds.

---

## Project Info

| Field | Details |
|---|---|
| **Subject** | Gen AI |
| **Tools** | Python, Vector DB, LLM API |
| **LLM** | Groq API (LLaMA 3.3 70B) |
| **Vector DB** | ChromaDB |
| **Agent Framework** | LangChain |

---

## Features

- **6 Report Types** — Site, Safety, Progress, Inspection, Daily, and Material Reports
- **Prompt Engineering** — Sophisticated templates ensure professional tone, formatting, and industry-standard terminology
- **Vector Database** — ChromaDB stores and retrieves past reports for improved consistency across generations
- **Planner Agent** — LangChain-powered multi-step reasoning agent that decomposes goals, validates resources via mock tools, and generates execution schedules
- **PDF Export** — Every generated report is automatically saved as a professionally formatted PDF
- **Web UI** — Clean, minimal dark-themed frontend served via Flask

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| LLM API | Groq API (LLaMA 3.3 70B Versatile) |
| Agent Framework | LangChain (`langchain`, `langchain-groq`) |
| Vector Database | ChromaDB |
| PDF Generation | ReportLab |
| Frontend | HTML, CSS, JavaScript |

---

## Project Structure

```
ConstructAI/
│
├── app/
│   ├── __init__.py
│   ├── generator.py          # Core LLM report generation
│   ├── planner_agent.py      # LangChain Planner Agent with tools
│   ├── prompts.py            # Prompt Engineering templates
│   ├── pdf_exporter.py       # ReportLab PDF export
│   └── vector_store.py       # ChromaDB vector storage
│
├── data/
│   └── exports/              # Generated PDF reports saved here
│
├── venv/                     # Python virtual environment
├── api.py                    # Flask API server (entry point)
├── index.html                # Frontend UI
├── main.py                   # CLI entry point
├── .env                      # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### Prerequisites

- Python 3.10 or above
- A free [Groq API Key](https://console.groq.com)

### Step 1 — Clone or open the project in VS Code

```bash
cd ConstructAI
```

### Step 2 — Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from [console.groq.com](https://console.groq.com).

### Step 5 — Run the application

```bash
python api.py
```

The browser will open automatically at `http://127.0.0.1:5000`.

> **Important:** Always use `http://127.0.0.1:5000` to open the app. Do NOT use VS Code's Live Server (port 5500) as it cannot connect to the Python backend.

---

## How to Use

### Generate a Report

1. Select a report type (Site, Safety, Progress, etc.)
2. Enter a construction topic (e.g., `concrete pouring on Level 3`)
3. Enter the site location (e.g., `Mumbai Site A`)
4. Click **Generate Report**
5. The report appears on screen and is saved as a PDF in `data/exports/`
6. Click **Download PDF** to download it

### Run the Planner Agent

1. Fill in the same fields as above
2. Click **Run Planner Agent**
3. The LangChain agent will autonomously:
   - Decompose the goal into actionable steps
   - Check worker, material, and equipment availability via tools
   - Validate site conditions
   - Generate a detailed execution schedule with dependencies
4. The final plan appears on screen and is also exported as a PDF

---

## Planner Agent — How It Works

The Planner Agent is built using **LangChain** with **Groq (LLaMA 3.3 70B)** as the LLM.

### Agent Tools (Mock Interfaces)

| Tool | Description |
|---|---|
| `check_workers_availability` | Returns available workers for a given role |
| `check_materials_availability` | Returns available quantities of construction materials |
| `check_equipment_availability` | Returns operational status of equipment |
| `validate_site_conditions` | Validates weather, permits, and access conditions |
| `generate_task_schedule` | Produces a step-by-step execution schedule with dependencies |

### Multi-Step Reasoning Loop

```
User Goal
    ↓
Decompose into steps
    ↓
Tool: check_workers_availability
    ↓
Tool: check_materials_availability
    ↓
Tool: check_equipment_availability
    ↓
Tool: validate_site_conditions
    ↓
Tool: generate_task_schedule
    ↓
Final Construction Plan (PDF)
```

The agent autonomously decides which tools to call and in what order, handling dependencies between steps dynamically.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend UI |
| `POST` | `/generate` | Generates a construction report |
| `POST` | `/plan` | Runs the Planner Agent |
| `GET` | `/download-pdf?path=...` | Downloads a generated PDF |

### POST `/generate` — Request Body

```json
{
  "topic": "concrete pouring on Level 3",
  "location": "Mumbai Site A",
  "report_type": "site_report"
}
```

### POST `/generate` — Response

```json
{
  "report": "Full report text...",
  "pdf": "data/exports/site_report_concrete_pouring_2026-04-18.pdf"
}
```

---

## Report Types

| Type | Key | Description |
|---|---|---|
| Site Report | `site_report` | General site overview, observations, and next steps |
| Safety Report | `safety_report` | Hazards, PPE compliance, incidents, and corrective actions |
| Progress Report | `progress_report` | Work completed vs planned, milestones, and delays |
| Inspection Report | `inspection_report` | Quality checks, defects, and approvals |
| Daily Report | `daily_report` | Daily activities, weather, workers, and equipment |
| Material Report | `material_report` | Materials received, used, wasted, and stock levels |

---

## Vector Database (ChromaDB)

Every report generated is stored in **ChromaDB**. When a new report is generated, the system:

1. Searches for similar past reports
2. Uses them as reference context in the prompt
3. Ensures consistency in tone and terminology across all reports

This means the application gets better and more consistent the more reports you generate.

---

## Requirements

```
flask
flask-cors
groq
chromadb==1.1.0
python-dotenv
reportlab
langchain==0.2.16
langchain-core==0.2.38
langchain-groq==0.1.9
langchain-community==0.2.16
```

To regenerate:
```bash
pip freeze > requirements.txt
```

---

## Known Notes

- Always run the app via `python api.py`, not Live Server
- ChromaDB data is stored in `.cache/chroma` and persists between sessions
- PDF files are saved in `data/exports/` and are never auto-deleted
- The Planner Agent may take 15–30 seconds due to multi-step reasoning

---

## License

This project was built for academic/educational purposes as part of a Gen AI course project.
