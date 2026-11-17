# Longitudinal Decision Memory Specification

## 1. The Need for Decision Memory

Traditional career recommendation systems treat each user interaction as a stateless, isolated query. If a student rejects a career, that preference is lost upon browser refresh or subsequent sessions.

DISHA AI introduces **Persistent Longitudinal Decision Memory**, which treats the student's career discovery as an evolving trajectory spanning days or weeks.

---

## 2. Tracked Decision Signals

1. **Explored Pathways**:
   - Every career viewed in deep-dive mode is recorded along with timestamps and time spent.
   - Prevents repetitively highlighting careers the student has already thoroughly vetted.

2. **Saved Shortlists**:
   - Careers the student bookmarks as high-affinity options for comparative analysis.

3. **Explicitly Rejected Paths with Rationale**:
   - When a student passes on a career (e.g. rejecting *Software Engineer* with rationale: *"I dislike 8 hours of solitary syntax coding"*), this rejection is permanently indexed as a **Negative Constraint**.
   - The recommendation and discovery engines incorporate these negative constraints into future rankings, down-weighting similar options and elevating careers emphasizing contrasting attributes (e.g., cross-functional collaboration, visual design).

4. **Counterfactual Simulation History**:
   - Logs simulated "What-If" hypotheses to identify latent interests and exploratory trends.

5. **Milestone Execution Progress**:
   - Tracks completed roadmap tasks, hours spent, and uploaded portfolio artifact URLs.

---

## 3. Storage Model (`StudentMemory`)

The `student_memories` table models longitudinal events:

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary key |
| `user_id` | `Integer` | Reference to student |
| `memory_type` | `String` | `career_explored`, `career_saved`, `career_rejected`, `what_if_simulated`, `roadmap_progress` |
| `career_id` | `String` | Associated career identifier |
| `content` | `Text` | Synthesized event narrative |
| `metadata` | `JSON` | Structured event attributes (rejection reason, parameters) |
| `created_at` | `DateTime` | Timestamp of event |

This event stream powers the interactive **Decision Timeline** in the UI and gives counselors and students a verifiable audit log of how their career clarity evolved over time.
