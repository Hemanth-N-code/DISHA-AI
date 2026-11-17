# DISHA AI 🧭

> **"DISHA: An Agentic AI Framework for Career Decision Exploration and Personalized Guidance"**  
> *Tagline: Discover Your Direction. Shape Your Future.*

[![License: MIT](https://img.shields.io/badge/License-MIT-indigo.svg)](LICENSE)
[![Python: 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com)
[![React: 18](https://img.shields.io/badge/React-18-61dafb.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178c6.svg)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8.svg)](https://tailwindcss.com)
[![Offline Capable](https://img.shields.io/badge/Deterministic_Offline-100%25-emerald.svg)]()

---

## 🌟 Core Research Novelty

Traditional career recommendation systems ask a narrow, static question:
> *"Given this student profile, which single career fits?"*

**DISHA AI introduces an iterative Career Decision-Exploration Framework asking:**
> *"What careers could this student consider, why do they fit, what alternatives exist, how will required skills transform with AI, what happens if the student chooses another path, and what actionable milestones should they conquer next?"*

```
CAREER RECOMMENDATION                  CAREER DECISION EXPLORATION (DISHA AI)
       (Static)                                      (Iterative)
+-------------------+                    +------------------------------------+
|  Student Profile  |                    | Dynamic Student Calibration Profile|
+---------+---------+                    +-----------------+------------------+
          |                                                |
          v                                                v
+-------------------+                    +------------------------------------+
| Black-box Top-1/3 |                    |  Diversity-Aware Universe Search   |
|   Assignment      |                    |     (CDI 0.88 vs 0.34 Baseline)    |
+---------+---------+                    +-----------------+------------------+
          |                                                |
          v                                                v
+-------------------+                    +------------------------------------+
|  Generic Roadmap  |                    | Alternative Pathway Graph (React Flow)
+-------------------+                    +-----------------+------------------+
                                                           |
                                                           v
                                         +------------------------------------+
                                         | Counterfactual "What-If" Simulator |
                                         +-----------------+------------------+
                                                           |
                                                           v
                                         +------------------------------------+
                                         | Deterministic Skill Gap & DAG Plan |
                                         +-----------------+------------------+
                                                           |
                                                           v
                                         +------------------------------------+
                                         | Longitudinal Decision Trace Memory |
                                         +------------------------------------+
```

### The 7 Core Architectural Pillars:
1. **Decision Exploration over Static Assignment**: Non-prescriptive recommendations preserving student self-efficacy.
2. **Career Diversity-Aware Discovery**: Defeats popularity bias using the **Career Diversity Index ($CDI$)**, covering 17 distinct occupational domains.
3. **Alternative Career Path Graph**: Interactive directed graph (powered by `@xyflow/react`) mapping lateral pivots and adjacent specializations.
4. **Counterfactual ("What-If") Simulator**: Sandbox for students to test non-linear perturbations ($\mathbf{p}' = \mathbf{p} + \mathbf{\Delta}$) without altering their permanent record.
5. **Career Transformation & AI Future-Resilience**: Decomposes typical work into **Automated**, **Augmented**, and **Human-Centered** task dimensions.
6. **Deterministic Skill Gap $\to$ Actionable Milestone DAG**: Translates identified skill gaps into 4 sequential execution stages with tangible portfolio artifacts.
7. **Persistent Longitudinal Decision Memory**: Tracks explored, saved, and explicitly rejected careers as negative constraints that refine future interactions.

---

## 🏗️ Architecture & Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript, Tailwind CSS, Vite | Responsive single-page application with modern glassmorphism UI |
| **Graph Visualizer**| `@xyflow/react` (React Flow) | Interactive directed career topology with lateral pivot bridges |
| **Data Visualization**| Recharts | Radar charts for skill gap vectors and bar charts for domain distributions |
| **Backend API** | FastAPI (Python 3.12), Pydantic v2 | High-throughput asynchronous REST API with strict schemas |
| **Database** | PostgreSQL + pgvector / SQLite Fallback | Dual persistence tier with zero-config local SQLite fallback |
| **Agent Orchestration**| LangGraph | Stateful multi-agent graph with Profile, Discovery, Analysis, and Roadmap agents |
| **Knowledge Base (RAG)**| In-memory TF-IDF / pgvector | Grounded on O*NET 2024, WEF Future of Jobs 2023, ESCO, and NEP 2020 |
| **LLM Service** | Google Gemini + Multi-Model Fallback | Powered by `gemini-flash-lite-latest` with instant deterministic offline fallback |
| **CET Counselling** | Karnataka KEA KCET Module | 59 Premier Karnataka colleges, 2023–2025 cutoffs, branch-to-career bridge |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.12+ (or 3.10+)
- Node.js 18+ & npm
- Docker & Docker Compose *(optional)*

---

### Option A: 1-Click Docker Compose Launch

Run the complete multi-container system (PostgreSQL + pgvector, FastAPI Backend, React Frontend):

```bash
docker-compose up --build
```
- **Frontend UI**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs

---

### Option B: Local Development Setup

#### 1. Full-Stack Single-Port Launch (Recommended)
```bash
# Navigate to backend and run with virtual environment
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open **http://127.0.0.1:8000** in your browser — FastAPI serves the compiled React production frontend, API endpoints (`/api/v1`), and Swagger docs (`/docs`) seamlessly from a single port.

#### 2. Dual-Terminal Development (with Vite HMR)
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```
- Frontend (Vite with hot-reload): http://localhost:5173
- Backend API & Docs: http://127.0.0.1:8000/docs

---

## 🎯 End-to-End Demo Walkthrough

Try the canonical student evaluation scenario:

1. **Quick Demo Login**:
   - Go to http://localhost:5173/login and click **"1-Click Demo Login"** (or use `disha-ai@gmail.com` / `DishaDemo2026!`).
2. **Onboarding / Pre-fill Scenario**:
   - Go to http://localhost:5173/onboarding and click **"Pre-fill Demo Scenario"**:
     - *Stream*: Science (PCM)
     - *Marks*: 86%
     - *Key Interests*: UI/UX Design, Visual Thinking, Human Psychology
     - *Programming*: Low
     - *Creativity*: High
3. **Career Universe Discovery**:
   - Explore the candidate grid with a **Career Diversity Index of 0.88**.
   - Notice that **UI/UX Designer** and **Human-Computer Interaction (HCI) Specialist** appear alongside analytical engineering roles with explicit `+` and `-` factor tags.
4. **Career Deep Dive & Task AI Impact**:
   - Click on **UI/UX Designer** to view 5-pillar compatibility, daily work, education paths, and task transformation (Wireframing automated/augmented vs. User Empathy 100% human).
5. **Alternative Path Graph**:
   - Click **"Explore Alternative Graph"** to inspect connected pivots (Product Manager, Front-End Developer, Interaction Designer) in the interactive React Flow canvas.
6. **Counterfactual "What-If" Simulation**:
   - Visit the **What-If Explorer**, tweak coding from *Low* to *None* and boost *Creativity*.
   - Watch the counterfactual delta engine classify surging vs. declined careers without altering your permanent profile.
7. **Side-by-Side Trade-Off Comparison**:
   - Select **UI/UX Designer** and **Data Scientist** in the 10-dimension comparator.
   - Review neutral observations highlighting the trade-offs in education duration, coding demands, and team dynamics.
8. **Deterministic Skill Gap & Actionable Roadmap**:
   - Inspect the Recharts Radar Chart showing current vs. target proficiencies.
   - Generate the **6-Month Actionable Milestone DAG** and check off tasks as they are completed.
9. **Decision Trace & IEEE Research Dashboard**:
   - Visit **Decision Memory** (`/journey`) to view your chronological event trace and recorded rejections.
   - Visit **IEEE Research Dashboard** (`/research`) to inspect quantitative metrics for $RQ_1-RQ_4$ publication.

---

## 🧪 Verification & Automated Tests

Run backend unit and integration test suites:
```bash
cd backend
pytest -v
```

### Test Coverage Highlights:
- `tests/test_auth.py`: JWT token issue, registration, bcrypt hashing.
- `tests/test_recommendation.py`: 5-pillar mathematical scoring, diversity optimization ($CDI$).
- `tests/test_what_if.py`: Counterfactual perturbation delta classification.
- `tests/test_skill_gap.py`: Deterministic proficiency difference matrix and priority categorization.

---

## 📚 Detailed Documentation

- [System Architecture](docs/architecture.md)
- [Recommendation Engine & Mathematical Formulation](docs/recommendation-engine.md)
- [Multi-Agent Workflow & LangGraph](docs/agent-workflow.md)
- [Retrieval-Augmented Generation (RAG)](docs/rag.md)
- [Longitudinal Decision Memory](docs/memory.md)
- [IEEE Research Evaluation Methodology](docs/research-evaluation.md)

---

## 📄 License
This project is open-source under the MIT License.
