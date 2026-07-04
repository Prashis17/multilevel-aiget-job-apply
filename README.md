# AI Job Application Automation System

Enterprise-style LangGraph application for job discovery, job analysis, recruiter discovery,
personalized outreach, Easy Apply automation, resume customization, tracking, and analytics.

This repository is intentionally modular. Portal-specific scraping and submission logic lives behind
interfaces so it can be hardened safely without changing the orchestration graph.

## Features

- LangGraph supervisor workflow with checkpoint-ready state.
- FastAPI backend for campaigns, jobs, applications, approvals, and analytics.
- SQLAlchemy repository layer with SQLite defaults and PostgreSQL-ready URLs.
- Playwright browser automation service with session persistence, screenshots, and manual captcha pause hooks.
- LLM provider abstraction for OpenAI, Gemini, Claude, and Ollama-compatible local models.
- YAML and dotenv configuration.
- Duplicate prevention with canonical keys and content hashes.
- Human approval gates for email, apply, and resume customization.
- Streamlit operations dashboard.
- Docker support and tests.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
playwright install chromium
copy .env.example .env
uvicorn app.main:app --reload
```

Dashboard:

```bash
streamlit run app/dashboard/streamlit_app.py
```

## Configuration

Edit `config/config.yaml` and `.env`. Secrets must stay in environment variables.

## Safety

This project does not hardcode credentials and does not bypass captcha or site protections. When
captcha, MFA, or low-confidence form fields are detected, the graph records a human approval task.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Testing](docs/TESTING.md)

