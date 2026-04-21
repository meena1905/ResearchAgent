# 🔍 ResearchAgent — Autonomous Founder & CEO Intelligence

> An autonomous AI research agent that investigates global tech leaders using multi-step reasoning, web search, and deep link exploration — built from scratch without LangChain or LangGraph.

---

## 🧠 How It Works

Unlike a simple web scraper, ResearchAgent uses a **3-Phase Autonomous Reasoning Loop**:

```
Phase 1: Broad Discovery
  └─ Generates 4 targeted search queries about the founder
  └─ Searches DuckDuckGo and collects snippets + URLs

Phase 2: Internal Reflection & Deep Dive
  └─ LLM reviews all snippets and identifies the most valuable URL
  └─ Scrapes that page in full for deep context (up to 4000 chars)
  └─ Stores findings in rolling memory (last 10 turns)

Phase 3: Structured Report Generation
  └─ LLM synthesizes everything into an 8-section Markdown report
  └─ Report saved to /output with source attribution log
```

---

## 📁 Project Structure

```
ResearchAgent/
│
├── agent.py               # Main agent pipeline
├── .env                   # API keys (not committed)
├── requirements.txt       # Dependencies
├── output/                # Generated reports saved here
│   └── sam_altman_report.md
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ResearchAgent.git
cd ResearchAgent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: [console.groq.com](https://console.groq.com)

---

## 🚀 Usage

```bash
python agent.py --founder "Sam Altman"
```

```bash
python agent.py --founder "Elon Musk"
```

```bash
python agent.py --founder "Sundar Pichai"
```

The agent will print its live progress and save the final report to the `output/` folder.

---

## 📄 Sample Output

Each generated report contains these sections:

| Section | Description |
|---|---|
| **Personal Background** | Early life, education, upbringing |
| **Career Journey** | Key roles and milestones |
| **Companies Founded / Led** | Organizations they built or lead |
| **Key Achievements & Awards** | Notable recognitions |
| **Leadership Style & Vision** | Philosophy and management approach |
| **Recent News & Developments** | Focus on 2025–2026 activity |
| **Notable Quotes** | Direct quotes attributed to the subject |
| **Summary** | 3-sentence assessment by the agent |

Plus an **Agent Navigation Log** listing all sources explored.

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| LLM Engine | Groq API — Llama 3.3 70B Versatile |
| Web Search | DuckDuckGo Search (duckduckgo-search) |
| Web Scraping | BeautifulSoup4 + Requests |
| Memory | Rolling in-context window (last 10 turns) |
| Orchestration | Pure Python — no LangChain, no LangGraph |
| Output Format | Structured Markdown reports |

---

## 📦 requirements.txt

```
requests
python-dotenv
duckduckgo-search
beautifulsoup4
```

---

## 🔑 Key Design Decisions

- **Framework-Free** — Entire agent loop built from scratch in Python. No LangChain or LangGraph dependency.
- **Rolling Memory** — The agent retains the last 10 conversation turns so context is preserved across phases without exceeding token limits.
- **2026-Aware** — Search queries explicitly target 2025–2026 developments to avoid stale information.
- **Reflection Step** — Before scraping, the LLM reflects on all snippets and picks the single most valuable URL — mimicking human research intuition.
- **Clean Scraping** — Scripts, styles, navbars, and footers are stripped before text extraction to reduce noise.

---

## ⚠️ Limitations

- Scraping is limited to publicly accessible pages (no login-gated content)
- Each scraped page is capped at 4000 characters to stay within token limits
- DuckDuckGo may occasionally rate-limit high-frequency searches
- Report quality depends on the availability of recent, high-quality web content about the subject

---
