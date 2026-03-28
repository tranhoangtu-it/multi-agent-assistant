# Multi-Agent Business Assistant

A portfolio project demonstrating a **lightweight multi-agent AI system** built from scratch using the raw OpenAI API — no CrewAI, no AutoGen, no LangChain.

---

## Features

- 3 specialised AI agents collaborating in a sequential pipeline
- 3 real-world business use cases out of the box
- Live agent progress tracking in the Streamlit UI
- Downloadable Markdown reports
- Fully async pipeline — fast and non-blocking
- Clean, testable architecture with dependency injection

---

## Architecture

```
User Input
    │
    ▼
┌─────────────────────────────────────────────────┐
│                  Orchestrator                   │
│                                                 │
│  ┌─────────────┐  context  ┌─────────────────┐  │
│  │ ResearchAgent│ ───────► │  AnalystAgent   │  │
│  │             │           │                 │  │
│  │ Gathers facts│          │ Finds patterns  │  │
│  │ & structures │          │ & quantifies    │  │
│  │ information  │          │ insights        │  │
│  └─────────────┘           └────────┬────────┘  │
│                                     │ context   │
│                                     ▼           │
│                            ┌─────────────────┐  │
│                            │   WriterAgent   │  │
│                            │                 │  │
│                            │ Synthesises to  │  │
│                            │ polished report │  │
│                            └─────────────────┘  │
└─────────────────────────────────────────────────┘
    │
    ▼
Final Report (Markdown)
```

---

## Use Cases

| Use Case | Input | Output |
|---|---|---|
| **Market Research** | Industry or topic | Market size, trends, players, opportunities, risks |
| **Competitor Analysis** | Company names (comma-separated) | Feature comparison, pricing, strengths/weaknesses |
| **Meeting Summary** | Raw transcript | Decisions, action items, owners, follow-up email |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-username/multi-agent-assistant.git
cd multi-agent-assistant

# 2. Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# 5. Run the app
streamlit run app.py
```

---

## Screenshot

> _Add screenshot here after first run_

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| LLM API | OpenAI (gpt-4o-mini) |
| UI | Streamlit |
| Async runtime | asyncio |
| Config | python-dotenv |
| Testing | pytest + pytest-asyncio |

---

## Agent Flow

```
1. ResearchAgent  →  Gathers comprehensive information on the topic
                     Structures findings: Overview, Key Facts, Trends, Sources

2. AnalystAgent   →  Receives research as context
                     Identifies patterns, compares, quantifies insights
                     Highlights top opportunities and risks

3. WriterAgent    →  Receives both research + analysis as context
                     Produces a polished Markdown report with:
                     Executive Summary, Findings, Recommendations
```

Each agent is a simple async wrapper around `client.chat.completions.create()` with a role-specific system prompt. The Orchestrator chains them together and emits progress events for the UI.

---

## Key Metrics

- **Automated 4-hour research into 10 minutes**
- 3 agents, 1 pipeline, 0 external frameworks
- ~300 lines of production code across all modules

---

## Project Structure

```
multi-agent-assistant/
├── agents/
│   ├── base_agent.py        # BaseAgent class
│   ├── research_agent.py    # ResearchAgent
│   ├── analyst_agent.py     # AnalystAgent
│   ├── writer_agent.py      # WriterAgent
│   └── orchestrator.py      # Pipeline coordinator
├── use_cases/
│   ├── market_research.py   # Prompt builder
│   ├── competitor_analysis.py
│   └── meeting_summary.py
├── tests/
│   ├── test_base_agent.py   # Agent + orchestrator tests
│   └── test_use_cases.py    # Use case prompt tests
├── app.py                   # Streamlit UI
├── requirements.txt
└── .env.example
```

---

## Running Tests

```bash
.venv/Scripts/python.exe -m pytest tests/ -v
```
