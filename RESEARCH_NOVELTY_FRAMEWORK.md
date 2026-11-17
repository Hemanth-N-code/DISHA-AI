# DISHA AI: Career Decision-Exploration Framework
## Formalized Research Novelty, Mathematical Formulation & System Architecture

---

### Executive Summary

Most existing automated career guidance systems published in literature formulate career recommendation as a **static, one-shot classification or ranking problem**:
$$f: \mathcal{X}_{\text{student}} \to \{c_1, c_2, \dots, c_k\} \subset \mathcal{C}$$

While effective at surfacing historically popular careers based on static profile matching, this paradigm fails real-world career planning because:
1. **Career discovery is inherently exploratory and cognitive**, not a single transactional transaction.
2. **Recommendation popularity bias** traps students in conventional fields (e.g., CS $\to$ Software Engineer), concealing high-affinity adjacent, emerging, or interdisciplinary domains.
3. **Static recommendations lack counterfactual agency**; students cannot explore *"What if I avoid heavy programming?"* or *"What if I invest in advanced mathematics?"*
4. **Market transformation is ignored**, treating occupations as static rather than evolving under AI and technological automation/augmentation.
5. **A recommendation without actionable continuity** creates high cognitive drop-off between career interest and tangible execution.

**DISHA AI** reformulates career guidance as an **Iterative, Multi-Objective Career Decision-Exploration Process** modeled over an **Alternative Career Path Graph**, bounded by **Diversity-Aware Discovery**, supported by **Counterfactual ("What-If") Optimization**, and anchored by **Longitudinal Decision Memory**.

---

## 1. Research Novelty Matrix: Conventional Recommenders vs. DISHA AI

| Dimension | Conventional IEEE Career Recommenders | DISHA AI Framework | Research Significance |
| :--- | :--- | :--- | :--- |
| **Core Problem Formulation** | One-shot static prediction / top-$k$ ranking | Interactive Multi-Turn Decision Exploration & Graph Traversal | Shifts from predictive ML to human-in-the-loop decision intelligence. |
| **Discovery Mechanism** | Cosine similarity / Collaborative filtering / Content-based matching | Multi-objective Diversity-Aware Discovery (Relevance + Domain Diversity + Serendipity) | Systematically breaks popularity bias; uncovers high-potential non-obvious career trajectories. |
| **Career Representation** | Discrete independent target classes / labels | Heterogeneous Directed Pathway Graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ with transition weights | Careers are navigable transit points with adjacent alternatives and transition costs. |
| **Interactivity & Agency** | Passive evaluation of fixed recommendations | Counterfactual ("What-If") Constraint Perturbation & Trajectory Recalculation | Evaluates trade-offs, preference shifts, and constraint relaxation dynamically. |
| **Market Relevance** | Historical role taxonomy (static O*NET / job codes) | Task-level Transformation Decomposition (Augmentation vs. Automation) | Integrates future skill viability and AI resilience into decision weights. |
| **Actionability** | Disconnected skill-gap checklist or static external course links | End-to-End Actionable Milestones (Skill Gap $\to$ Priority $\to$ Project DAG $\to$ Readiness) | High-fidelity translation from cognitive decision to structured execution. |
| **Session Continuity** | Stateless sessions (cold-start reset upon each visit) | Persistent Longitudinal Decision Trace (Preferences, Rejected Nodes, Exploration Path) | Context-aware decision evolution over months/semesters. |

---

## 2. Detailed Mathematical & Algorithmic Formalization

### Novelty 1: Iterative Decision-Exploration Formulation
Instead of a single mapping $f(\mathcal{X})$, career discovery is modeled as a stateful exploration trajectory:
$$\mathcal{S}_t = \langle \mathcal{U}_t, \mathcal{C}_{\text{active}}, \mathcal{H}_{t}, \mathcal{K}_t \rangle$$
Where:
- $\mathcal{U}_t$: User state at step $t$ (skills, affinities, education, cognitive interests).
- $\mathcal{C}_{\text{active}}$: Current set of candidate careers under inspection.
- $\mathcal{H}_t$: Exploration history (inspected, compared, bookmarked, and explicitly rejected paths).
- $\mathcal{K}_t$: Active constraint vector (e.g., location, academic timeline, programming aversion, math tolerance).

Transition function:
$$\mathcal{S}_{t+1} = \mathcal{T}(\mathcal{S}_t, a_t)$$
where $a_t \in \mathcal{A}$ represents user actions: `[Inspect, ExploreAlternatives, ApplyConstraint, Compare, AnalyzeGap, Commit]`.

---

### Novelty 2: Career Diversity-Aware Discovery & CDI Metric

#### Problem: Popularity & Homogeneity Bias
Standard recommenders maximize pure similarity:
$$\arg\max_{c \in \mathcal{C}} \text{Sim}(\mathbf{e}_u, \mathbf{e}_c)$$
leading to domain clustering (e.g., all recommended careers falling under pure software development).

#### DISHA Discovery Objective:
Let $\mathcal{R} = \{c_1, c_2, \dots, c_k\}$ be the set of surfaced careers. The objective function balances affinity, diversity, and serendipity:
$$\mathcal{L}_{\text{discovery}}(\mathcal{R}) = \sum_{c \in \mathcal{R}} \text{Relevance}(u, c) + \lambda \cdot \text{Div}(\mathcal{R}) + \gamma \cdot \text{Serendipity}(u, \mathcal{R})$$

Where:
1. **Relevance**: Cosine similarity between user embedding $\mathbf{e}_u$ and career requirement embedding $\mathbf{e}_c$.
2. **Intra-List Diversity ($\text{Div}$)**:
   $$\text{Div}(\mathcal{R}) = \frac{2}{k(k-1)} \sum_{i=1}^{k} \sum_{j=i+1}^{k} \left(1 - \text{CosineSim}(\mathbf{d}_{c_i}, \mathbf{d}_{c_j})\right)$$
   where $\mathbf{d}_c$ is the domain taxonomy embedding of career $c$.
3. **Serendipity**: Measures novel, unexpected relevance (relevance of career $c$ to user $u$ scaled by the unexpectedness relative to standard baseline expectations).

#### Career Diversity Index (CDI) Formulation for Evaluation:
To measure performance in experiments:
$$\text{CDI}(\mathcal{R}) = \frac{|\text{UniqueDomains}(\mathcal{R})|}{|\mathcal{R}|} \times \left( - \sum_{d \in \mathcal{D}_{\mathcal{R}}} p(d) \log_2 p(d) \right)$$
Combining domain span with domain entropy $H(\mathcal{D}_{\mathcal{R}})$.

---

### Novelty 3: Alternative Career Path Graph $\mathcal{G}_{\text{career}}$

DISHA constructs a Heterogeneous Directed Knowledge Graph:
$$\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{W})$$
- **Vertices $\mathcal{V}$**:
  - $\mathcal{V}_{\text{career}}$: Occupations/Roles
  - $\mathcal{V}_{\text{skill}}$: Core, technical, and human competencies
  - $\mathcal{V}_{\text{domain}}$: Industry sectors & knowledge verticals
- **Edges $\mathcal{E}$**:
  - $(c_i, c_j, \text{AdjacentTo})$: Lateral mobility / alternative pathways
  - $(c_i, s_k, \text{RequiresSkill})$: Skill dependency
  - $(c_i, d_m, \text{BelongsToDomain})$: Domain categorization
  - $(c_i, c_j, \text{UpwardPath})$: Vertical progression
- **Edge Weights $\mathcal{W}$**:
  $$W(c_i \to c_j) = \text{TransitionCost}(c_i, c_j) = \sum_{s \in \text{Skills}(c_j) \setminus \text{Skills}(c_i)} \text{Difficulty}(s)$$

When a student inspects career $C_A$, the alternative pathway engine traverses adjacent nodes where $W(C_A \to C_B) < \theta$, exposing viable pivot pathways without starting from zero.

---

### Novelty 4: Counterfactual ("What-If") Constraint Exploration

Given user state $\mathcal{U} = \langle \mathbf{x}_{\text{skills}}, \mathbf{x}_{\text{preferences}}, \mathbf{x}_{\text{constraints}} \rangle$:
A counterfactual query defines a perturbation $\delta$:
$$\mathcal{U}' = \mathcal{U} \oplus \delta$$
Examples:
- $\delta = \{\text{programming\_affinity} \gets \text{LOW}\}$
- $\delta = \{\text{quantitative\_willingness} \gets \text{HIGH}\}$
- $\delta = \{\text{domain\_exclusion} \gets \{\text{Finance}\}\}$

DISHA calculates the **Pareto Career Shift**:
$$\Delta \mathcal{C} = \text{TopK}(\mathcal{U}') \setminus \text{TopK}(\mathcal{U})$$
And generates the **Pivot Explanation**:
$$\text{Explain}(\Delta \mathcal{C}) = \left\{ \text{Factor: } \delta, \text{ Unlocked: } \Delta \mathcal{C}, \text{ Tradeoffs: } \text{TopK}(\mathcal{U}) \setminus \text{TopK}(\mathcal{U}') \right\}$$

---

### Novelty 5: Career Transformation & Future-Skill Resilience

Occupations are decomposed into fine-grained tasks $\mathcal{T}(c) = \{t_1, t_2, \dots, t_n\}$.
For each task $t_i$:
- **$P_{\text{auto}}(t_i)$**: Probability of task automation by emerging technologies.
- **$P_{\text{aug}}(t_i)$**: Probability of task augmentation (AI-assisted execution).
- **$S_{\text{resilient}}(t_i)$**: Complementary human capability required (e.g., architectural judgment, high-stakes verification, domain empathy).

The career's **Future Skill Resilience Score (FSRS)**:
$$\text{FSRS}(c) = \frac{\sum_{s \in \text{EmergingSkills}(c)} \text{Importance}(s, c)}{\sum_{s \in \text{TraditionalSkills}(c)} \text{AutomationRisk}(s)}$$
The student is not presented with alarming binary statements ("This job will vanish"), but with a task-transformation matrix identifying which skills to prioritize for long-term viability.

---

### Novelty 6: End-to-End Decision Continuity (Gap $\to$ Actionable DAG)

Skill gap analysis produces an actionable Directed Acyclic Graph (DAG) of learning and execution:
$$\mathcal{M} = (\mathcal{V}_{\text{milestones}}, \mathcal{E}_{\text{prerequisites}})$$
Where each node $m \in \mathcal{V}_{\text{milestones}}$ contains:
- **Target Skill**: $s \in \text{Gap}(\mathcal{U}, c^*)$
- **Pedagogical Modality**: Concept $\to$ Application $\to$ Capstone
- **Artifact Output**: Tangible portfolio proof (e.g., GitHub repository, UX case study, research writeup)
- **Estimated Horizon**: Time-to-mastery in weeks based on baseline proficiency

---

### Novelty 7: Persistent Longitudinal Decision Trace

Memory is structured into a stateful schema:
```json
{
  "student_id": "STU_2026_901",
  "active_intent": "Product Design / HCI",
  "explored_nodes": ["Software Engineering", "UX Research", "Product Management"],
  "rejected_nodes": [
    {
      "career": "Backend Engineering",
      "timestamp": "2026-09-16",
      "explicit_rationale": "Dislikes heavy algorithm implementation and low-level debugging",
      "inferred_constraint": "prefer_visual_and_human_interaction"
    }
  ],
  "evaluated_counterfactuals": [
    { "what_if": "Remove heavy math", "resulting_interest": "Technical Writing, UX" }
  ],
  "milestone_progress": {
    "completed": ["Figma Fundamentals", "User Interview Methodologies"],
    "in_progress": ["Usability Testing Portfolio Piece"]
  }
}
```
In subsequent sessions, DISHA initializes from the **Decision Trace**, preventing repetitive cycles and deepening exploration.

---

## 3. Unified Architectural Blueprint

```
                      ┌─────────────────────────────────┐
                      │          STUDENT USER           │
                      └────────────────┬────────────────┘
                                       │ Interactive Input / Goals
                                       ▼
                      ┌─────────────────────────────────┐
                      │    Decision Trajectory Engine   │
                      │   (State, Actions, Preferences) │
                      └───────┬─────────────────┬───────┘
                              │                 │
            Constraint Filter │                 │ Exploration Query
                              ▼                 ▼
             ┌─────────────────────────┐  ┌─────────────────────────┐
             │ Diversity-Aware Scorer  │  │ Alternative Path Graph  │
             │ (Relevance + CDI + Ser) │  │  (Heterogeneous Graph)   │
             └────────────┬────────────┘  └────────────┬────────────┘
                          │                            │
                          └─────────────┬──────────────┘
                                        ▼
                      ┌─────────────────────────────────┐
                      │    What-If Counterfactual Core  │
                      │  (Perturbation & Tradeoff Eval) │
                      └────────────────┬────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │  Transformation & Future Skills │
                      │  (Augmentation/Automation Risk) │
                      └────────────────┬────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │  Skill-Gap to Milestone DAG Gen │
                      │  (Portfolio-Centric Roadmap)    │
                      └────────────────┬────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │ Persistent Decision Memory DB   │
                      │   (Longitudinal State Trace)    │
                      └─────────────────────────────────┘
```

---

## 4. Suggested IEEE Paper Structure & Research Questions

### Formal Research Questions (RQs)
- **$RQ_1$ (Discovery Diversity)**: Does the Diversity-Aware Discovery algorithm significantly increase Career Diversity Index (CDI) and reveal non-obvious career options without degrading recommendation relevance compared to conventional collaborative/content-based baselines?
- **$RQ_2$ (Decision Confidence & Agency)**: How does the Alternative Path Graph and What-If counterfactual exploration impact students' decision clarity, exploratory confidence, and perceived agency compared to static top-$k$ career recommendations?
- **$RQ_3$ (Future-Readiness Alignment)**: Does integrating task-level transformation and future-skill analysis alter students' career trajectory choices toward higher-resilience skills?
- **$RQ_4$ (Action Continuity)**: Does translating career selection directly into a portfolio-centric milestone DAG improve follow-through and goal-setting clarity compared to standalone skill checklists?

### Suggested IEEE Target Conferences / Journals
- **IEEE Transactions on Learning Technologies (TLT)**
- **IEEE Conference on Learning International Networks for Knowledge (LINK) / FIE (Frontiers in Education)**
- **IEEE Access** (Special Section on AI in Education / Recommender Systems)
- **ACM RecSys** / **ACM IUI (Intelligent User Interfaces)** (Human-Centered Recommender Systems)
