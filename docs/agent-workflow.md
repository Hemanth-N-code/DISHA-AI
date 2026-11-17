# Multi-Agent Workflow & LangGraph Orchestration

## 1. Agent Architecture

DISHA AI coordinates four specialized agents organized within a stateful **LangGraph** execution graph:

```
[Student Request / Calibration]
              |
              v
     +-----------------+
     |  Profile Agent  | ----> Validates profile, extracts cognitive constraints
     +--------+--------+
              |
              v
    +-------------------+
    |  Discovery Agent  | ----> Evaluates 5-pillar scores & optimizes CDI coverage
    +---------+---------+
              |
              v
    +-------------------+
    |   Analysis Agent  | ----> Evaluates skill gaps & task automation resilience
    +---------+---------+
              |
              v
    +-------------------+
    |   Roadmap Agent   | ----> Constructs 4-stage milestone DAG with artifacts
    +-------------------+
```

---

## 2. Agent Responsibilities

### 1. Profile Agent (`profile_agent.py`)
- **Role**: Validates that required student academic inputs are complete (12th stream, marks, subjects).
- **Inference**: Analyzes raw student text inputs to extract latent interests and cognitive orientations.
- **Synthesis**: Generates the personalized Archetype Summary (e.g. *"Analytical Creator with high quantitative aptitude and visual empathy"*).

### 2. Discovery Agent (`discovery_agent.py`)
- **Role**: Coordinates career universe exploration.
- **Operation**:
  - Invokes the deterministic 5-pillar recommendation engine.
  - Applies the Career Diversity Index ($CDI$) optimization algorithm to ensure cross-domain breadth.
  - Generates transparent, agency-preserving Factor Tags (`+ Positive`, `- Cautionary`) explaining the exact drivers of compatibility.

### 3. Analysis Agent (`analysis_agent.py`)
- **Role**: Conducts deep-dive examination of individual career pathways.
- **Operation**:
  - Runs deterministic skill gap matrix computations.
  - Decomposes typical work into **Automated Tasks** (routine tasks AI can handle), **Augmented Tasks** (tasks where AI boosts human capability), and **Human-Centered Tasks** (empathy, strategy, creative judgement).
  - Retrieves grounded citations from O*NET and WEF labor reports.

### 4. Roadmap Agent (`roadmap_agent.py`)
- **Role**: Transforms abstract career goals into sequential action.
- **Operation**:
  - Maps identified skill gaps to concrete learning milestones across 4 distinct stages.
  - Assigns estimated completion timelines in weeks.
  - Associates tangible portfolio artifact deliverables (e.g., GitHub repos, Figma prototypes, research essays) for every major task.

---

## 3. LangGraph State Definition

The pipeline operates on a unified typed state dictionary:

```python
class CareerWorkflowState(TypedDict):
    user_id: int
    profile: StudentProfileResponse
    selected_career_id: Optional[str]
    candidates: List[CareerCandidate]
    skill_gap: Optional[SkillGapResponse]
    roadmap: Optional[RoadmapResponse]
    memory_context: Dict[str, Any]
    errors: List[str]
```

### Fault Tolerance & Offline Recovery
Each agent node incorporates safe try-catch recovery. If an external LLM API fails or times out, the node automatically delegates to `llm_service.py`'s deterministic rule-based synthesizer, guaranteeing 100% uptime and offline viability without crashing the pipeline.
