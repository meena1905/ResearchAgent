# ResearchAgent: Autonomous Founder & CEO Intelligence

An advanced autonomous research agent designed to "navigate, explore, and organize insights" about global tech leaders.

Developed for the AI Agent Developer Internship at LegalSeva.org.

## Agent Architecture

Unlike static scrapers, this agent uses a **Multi-Step Reasoning Loop** to autonomously investigate a subject:

- **Query Generation** — The agent analyzes the target's name and generates targeted search queries  
  (e.g., "Sam Altman recent investments 2026", "Sam Altman leadership philosophy")

- **Autonomous Navigation** — Identifies high-value technical and news URLs from DuckDuckGo search results  

- **Deep Exploration** — Follows links and scrapes detailed content using BeautifulSoup4, going beyond surface-level summaries  

- **Internal Reflection** — Reviews gathered data to identify information gaps or contradictions  

- **Synthesis** — Structures information into a professional Markdown report with source attribution and focus on 2025–2026 developments  

## Key Features

- **Framework-Free Orchestration** — Built from scratch using Python and Groq (Llama 3.3 70B)  
- **2026-Aware** — Prioritizes recent news and up-to-date information  
- **Structured Outputs** — Generates clean Markdown reports with headers, bullet points, and citations  

## Setup & Installation

1. Install dependencies:
```bash
pip install -r requirements.txt