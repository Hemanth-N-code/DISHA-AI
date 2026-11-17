# DISHA AI Architecture Specification

## 1. System Overview

**DISHA AI** ("DISHA: An Agentic AI Framework for Career Decision Exploration and Personalized Guidance") is an end-to-end, full-stack decision-support system designed for students completing 12th / Intermediate / PUC education.

Rather than treating career guidance as a static, one-shot classification or top-$k$ recommendation task, DISHA models career discovery as an **iterative exploration process across a multi-dimensional decision space**.

```
                           +------------------------+
                           |  Student Profile &     |
                           |  Decision Memory       |
                           +-----------+------------+
                                       |
                                       v
                     +------------------------------------+
                     |  LangGraph Agentic Orchestrator    |
                     +-----------------+------------------+
                                       |
        +------------------------------+------------------------------+
        |                              |                              |
        v                              v                              v
+---------------+             +-----------------+             +---------------+
| Profile Agent |             | Discovery Agent |             | Roadmap Agent |
| (Calibration) |             | (CDI Selection) |             | (DAG Planner) |
+---------------+             +--------+--------+             +---------------+
                                       |
                                       v
                           +------------------------+
                           | Deterministic Engines: |
                           | 1. 5-Pillar Compatibility
                           | 2. Counterfactual Perturbation
                           | 3. Skill Gap & Graph Topology
                           +-----------+------------+
                                       |
                                       v
                           +------------------------+
                           | Grounded RAG Service   |
                           | (O*NET, WEF, AISHE)    |
                           +-----------+------------+
                                       |
                                       v
               +------------------------------------------------+
               | Modern Interactive Frontend (React + TS):      |
               | - Decision Universe & CDI Badge                |
               | - Directed Alternative Path Graph (React Flow) |
               | - Counterfactual What-If Simulator             |
               | - 10-Dimension Side-by-Side Comparator         |
               | - Deterministic Skill Gap Radar/Bar Charts     |
               | - 4-Stage Execution Roadmap with Artifacts     |
               | - Longitudinal Journey Trace & IEEE Dashboard  |
               +------------------------------------------------+
```

---

## 2. Decoupled Core Philosophy: Deterministic Core vs. Generative Layer

To eliminate LLM hallucinations and enforce empirical validity, DISHA strictly separates its execution into two layers:

1. **Deterministic Layer (Mathematical & Rule-Based)**:
   - **5-Pillar Scoring Engine**: Calculates bounded compatibilities $\in [0, 100]$ using predefined weights ($w_{\text{interest}}, w_{\text{academic}}, w_{\text{skill}}, w_{\text{pref}}, w_{\text{goal}}$).
   - **Diversity-Aware Candidate Selector**: Maximizes domain entropy via the Career Diversity Index ($CDI$) to prevent algorithmic popularity bias.
   - **What-If Perturbation Engine**: Evaluates counterfactual scenario vectors ($\mathbf{p}' = \mathbf{p} + \mathbf{\Delta}$) deterministically without corrupting the student's persistent profile.
   - **Skill Gap Analyzer**: Evaluates difference matrices $\text{Gap}(s) = \max(0, R(s) - C(s))$ on a discrete 1-5 proficiency scale.
   - **React Flow Graph Builder**: Computes topological coordinate layouts for focal careers, lateral pivots, and adjacent specializations.

2. **Generative Layer (Language Models & RAG)**:
   - Synthesizes personalized contextual explanations.
   - Extracts semantic student intents from conversational queries.
   - Summarizes grounded labor-market context from O*NET 2024 and WEF Future of Jobs reports without hallucination.
   - Generates nuanced task transformation profiles (Automated vs. Augmented vs. Human-Centered).

---

## 3. Data & Storage Tier

- **Primary Database**: PostgreSQL with `pgvector` extension for semantic embedding retrieval.
- **Local Fallback Engine**: SQLite (`disha.db`) with automated zero-config fallback if PostgreSQL is unavailable.
- **Relational Models**:
  - `User`: Identity, authentication credentials (bcrypt hashed).
  - `StudentProfile`: 5-pillar student attributes, skills list (1-5), cognitive preferences, and goals.
  - `Career`: 118 catalog careers across 17 domains with tasks, skill vectors, pivots, and AI impacts.
  - `Roadmap` & `RoadmapTask`: Milestone DAG tracking status (`not_started`, `in_progress`, `completed`) and artifact URLs.
  - `StudentMemory`: Persistent longitudinal events (explored careers, saved bookmarks, rejected options with rationale).
  - `ResearchEvent` & `ResearchMetricSnapshot`: Experimental metrics tracking for academic publication.

---

## 4. Multi-Agent Orchestration via LangGraph

The orchestration pipeline is implemented as a state graph (`StateGraph(CareerWorkflowState)`):

- **`CareerWorkflowState`**:
  - `user_id`: Current student identifier.
  - `profile`: Extracted student profile.
  - `selected_career_id`: Target career in focus.
  - `candidates`: Ranked and diversity-selected career candidates.
  - `skill_gap`: Gap analysis result.
  - `roadmap`: Generated milestone DAG.
  - `memory_context`: Longitudinal history of explorations and rejections.
  - `errors`: Resilient error logs and recovery messages.

- **Nodes & State Transitions**:
  1. `profile_node` $\to$ Verifies profile completeness and extracts implicit constraints.
  2. `discovery_node` $\to$ Runs 5-pillar scoring and diversity optimization.
  3. `analysis_node` $\to$ Runs skill gap analysis and task-level AI impact decomposition.
  4. `roadmap_node` $\to$ Generates structured, milestone-driven sequential roadmap.
