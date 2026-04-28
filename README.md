# ConstructAI — Construction Content Generator

> A specialized GenAI-powered platform that transforms basic construction topics into professional, industry-standard documentation using advanced Prompt Engineering, a Planner Agent, and Vector DB memory.

---

## Live Deployment

| Environment | URL | Status |
|---|---|---|
| Docker Compose | [http://47.128.153.137:5000](http://47.128.153.137:5000) | ✅ Healthy |
| Kubernetes | [http://47.128.153.137:5001](http://47.128.153.137:5001) | ✅ Running |

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started (Local)](#getting-started-local)
- [Docker Setup](#docker-setup)
- [Kubernetes Setup](#kubernetes-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [API Endpoints](#api-endpoints)
- [Report Types](#report-types)
- [Planner Agent](#planner-agent)

---

## Project Overview

ConstructAI is a full-stack Generative AI application built for construction professionals. It uses **Prompt Engineering**, a **LangChain Planner Agent**, and **ChromaDB vector memory** to generate consistent, professional construction reports. The application is containerized with Docker, orchestrated with Kubernetes, and deployed on AWS EC2 with automated CI/CD via GitHub Actions.

---

## Features

- **6 Report Types** — Site, Safety, Progress, Inspection, Daily, Material
- **Planner Agent** — LangChain-powered multi-step reasoning agent with 5 mock tools
- **Vector Memory** — ChromaDB stores past reports for consistency across generations
- **PDF Export** — Professional PDF generation via ReportLab
- **Dark UI** — Responsive HTML/CSS/JS frontend served via Flask
- **Containerized** — Multi-stage Docker build with security best practices
- **Orchestrated** — Kubernetes deployment with ConfigMap and Secrets
- **CI/CD** — GitHub Actions auto-deploys to EC2 on every push

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM API | Groq API (LLaMA 3.3-70B) |
| Agent Framework | LangChain (`AgentExecutor`, `create_tool_calling_agent`) |
| Vector DB | ChromaDB (PersistentClient) |
| Backend | Python, Flask, Flask-CORS |
| PDF Generation | ReportLab |
| Frontend | HTML, CSS, JavaScript |
| Containerization | Docker (multi-stage Dockerfile) |
| Orchestration | Kubernetes (minikube), kubectl |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 (t3.small, Singapore region) |
| Version Control | Git, GitHub |

---

## Project Structure

```
ConstructAI/
│
├── app/
│   ├── __init__.py
│   ├── generator.py          # Core LLM generation logic (Groq API)
│   ├── vector_store.py       # ChromaDB vector memory
│   ├── prompts.py            # Prompt engineering templates (6 report types)
│   ├── pdf_exporter.py       # ReportLab PDF generation
│   └── planner_agent.py      # LangChain Planner Agent with 5 tools
│
├── data/
│   ├── exports/              # Generated PDF reports saved here
│   └── chromadb/             # Persistent ChromaDB vector storage
│
├── k8s/
│   ├── deployment.yaml       # Kubernetes Deployment config
│   ├── service.yaml          # Kubernetes NodePort Service
│   └── configmap.yaml        # Environment configuration
│
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions CI/CD pipeline
│
├── api.py                    # Flask API server (entry point)
├── index.html                # Frontend UI
├── Dockerfile                # Multi-stage Docker build
├── docker-compose.yml        # Docker Compose orchestration
├── .dockerignore             # Docker build exclusions
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not committed)
└── README.md
```

---

## Getting Started (Local)

### Prerequisites

- Python 3.11+
- Git
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ConstructAI.git
cd ConstructAI

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_key_here > .env

# Run the app
python api.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Docker Setup

### Build and Run

```bash
# Build and start container
docker compose up --build -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop container
docker compose down
```

### Useful Docker Commands

```bash
# List images
docker images

# Container stats
docker stats

# Execute shell inside container
docker exec -it constructai-app bash

# Health check
docker exec constructai-app curl http://localhost:5000
```

### Dockerfile — Multi-stage Build

The Dockerfile uses a **2-stage build** for optimized image size and security:

- **Stage 1 (Builder)** — Installs all Python dependencies
- **Stage 2 (Production)** — Copies only built packages, runs as non-root `appuser`, includes `curl` for healthcheck

This reduces attack surface and keeps the final image lean.

---

## Kubernetes Setup

### Prerequisites

```bash
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Start cluster
minikube start --driver=docker
```

### Deploy

```bash
# Build image directly inside minikube (avoids OOM on t3.small)
eval $(minikube docker-env)
docker build -t constructai:latest .

# Create secret
kubectl create secret generic constructai-secret \
  --from-literal=GROQ_API_KEY=your_groq_api_key_here

# Apply configs
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Verify

```bash
kubectl get pods           # Pod status
kubectl get deployments    # Deployment status
kubectl get services       # Service + NodePort
kubectl logs deployment/constructai-deployment
kubectl describe deployment constructai-deployment
```

### Access via Port Forward

```bash
# Run in background
nohup kubectl port-forward service/constructai-service 5001:5000 --address 0.0.0.0 &

# Access at
# http://YOUR_EC2_IP:5001
```

---

## CI/CD Pipeline

GitHub Actions automatically runs on every push to `main`.

### Pipeline Stages

| Stage | What it does |
|---|---|
| Checkout | Pulls latest code |
| Setup Python | Installs Python 3.11 |
| Install Dependencies | Runs `pip install -r requirements.txt` |
| Syntax Check | Validates all Python files compile |
| Build Docker Image | Builds `constructai:latest` |
| Verify Image | Confirms image exists |
| Deploy to EC2 | SSHs into EC2, pulls code, rebuilds container |

### Secrets Required in GitHub

Go to `Settings → Secrets → Actions` and add:

| Secret | Value |
|---|---|
| `EC2_HOST` | Your EC2 public IP |
| `EC2_SSH_KEY` | Contents of your `.pem` file |

### View Pipeline

```
https://github.com/YOUR_USERNAME/ConstructAI/actions
```

---

## AWS EC2 Deployment

### Instance Details

| Setting | Value |
|---|---|
| Instance Type | t3.small |
| Region | Asia Pacific (Singapore) ap-southeast-1 |
| OS | Ubuntu 22.04 LTS |
| Storage | 8 GB |

### Security Group Inbound Rules

| Port | Purpose |
|---|---|
| 22 | SSH access |
| 5000 | Docker Compose app |
| 5001 | Kubernetes port-forward |
| 30001 | Kubernetes NodePort |

### Connect to EC2

```bash
ssh -i constructai-key.pem ubuntu@YOUR_EC2_IP
```

### Cost Management

```
t3.small = ~$0.025/hour
Always STOP (not terminate) instance when not in use
Estimated cost for demo usage = ~$0.20/day
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves frontend UI |
| `POST` | `/generate` | Generate construction report |
| `POST` | `/plan` | Run Planner Agent |
| `GET` | `/download-pdf` | Download generated PDF |

### POST `/generate`

```json
{
  "topic": "concrete pouring on Level 3",
  "location": "Mumbai Site A",
  "report_type": "site_report"
}
```

### POST `/plan`

```json
{
  "topic": "fire extinguisher installation",
  "location": "Delhi Mall",
  "report_type": "safety_report"
}
```

---

## Report Types

| Key | Report | Description |
|---|---|---|
| `site_report` | Site Report | General site overview and observations |
| `safety_report` | Safety Report | Hazards, PPE compliance, incidents |
| `progress_report` | Progress Report | Work done vs planned, milestones, delays |
| `inspection_report` | Inspection Report | Quality checks, defects, approvals |
| `daily_report` | Daily Report | Day's activities, workers, weather |
| `material_report` | Material Report | Materials received, used, wasted |

---

## Planner Agent

The Planner Agent is built with **LangChain** + **Groq API** and uses a multi-step reasoning loop to autonomously orchestrate construction tasks.

### How it works

1. **Decomposes** the high-level goal into 4–6 actionable steps
2. **Checks** worker availability via mock tool
3. **Validates** materials and equipment via mock tools
4. **Validates** site conditions via mock tool
5. **Generates** an execution schedule with dependencies via mock tool
6. **Produces** a final structured construction plan

### Tools Available to Agent

| Tool | Purpose |
|---|---|
| `check_workers_availability` | Check available workers by role |
| `check_materials_availability` | Check material stock levels |
| `check_equipment_availability` | Check equipment operational status |
| `validate_site_conditions` | Validate site is approved for work |
| `generate_task_schedule` | Generate time-based execution schedule |

### LangChain Components Used

```python
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Never commit `.env` to Git. It is listed in `.gitignore`.

---

## Known Issues & Fixes Applied

| Issue | Fix |
|---|---|
| `pywin32` in requirements.txt (Windows-only) | Replaced with minimal Linux-compatible requirements |
| ChromaDB permission error on mounted volume | `chmod -R 777 data/` on EC2 host |
| `/home/appuser/.cache` permission error | Added `mkdir` + `chown` in Dockerfile |
| Hardcoded `127.0.0.1:5000` in frontend | Replaced with relative URLs (`/generate`, `/plan`) |
| `minikube image load` OOM on t3.small | Used `eval $(minikube docker-env)` + build directly |
| Port 5000 conflict between Docker and K8s | K8s port-forwarded to 5001 instead |
| Container unhealthy (`curl` missing) | Added `curl` install in production stage of Dockerfile |

---

## Acknowledgements

- [Groq](https://groq.com) — Free LLM API (LLaMA 3.3-70B)
- [LangChain](https://langchain.com) — Agent framework
- [ChromaDB](https://trychroma.com) — Vector database
- [ReportLab](https://reportlab.com) — PDF generation
- [Medicaps University](https://medicaps.ac.in) — GenAI Skill-Based Course