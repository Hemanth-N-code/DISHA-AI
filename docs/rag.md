# Retrieval-Augmented Generation (RAG) Architecture

## 1. Grounded Knowledge Base

To ensure that career guidance is grounded in empirical labor market reality rather than speculative LLM generations, DISHA indexes a comprehensive database of **118 verified career profiles** across **17 distinct domains**.

Each career entry contains:
- Official standard occupational classification codes and taxonomy.
- Granular daily tasks and cognitive demands.
- Required skills calibrated on a discrete 1 to 5 proficiency scale.
- Alternative lateral pivots and adjacent specializations.
- Authoritative source citations:
  - **O*NET 2024 Content Model** (U.S. Department of Labor)
  - **World Economic Forum (WEF) Future of Jobs Report 2023**
  - **European Skills, Competences, Qualifications and Occupations (ESCO)**
  - **National Education Policy (NEP) 2020 Guidelines**
  - **All India Survey on Higher Education (AISHE 2024)**

---

## 2. Vector Store & Retrieval Pipeline

DISHA supports two dual retrieval implementations:

1. **In-Memory TF-IDF Cosine Vector Store** (`vector_store.py`):
   - Tokenizes career descriptions, domains, tasks, and skill sets.
   - Computes weighted Term Frequency-Inverse Document Frequency matrices.
   - Enables blazing fast (< 5ms), zero-dependency semantic vector similarity search completely offline.

2. **PostgreSQL pgvector Store** (for Production Deployment):
   - Uses vector embeddings (OpenAI `text-embedding-3-small` or HuggingFace `all-MiniLM-L6-v2`).
   - Indexes embeddings using IVFFlat or HNSW cosine distance indexing in PostgreSQL.

---

## 3. Grounded Prompting & Non-Hallucinatory Generation

When a student queries the DISHA Career Counselor AI:

1. The retrieval pipeline queries the vector store for top-$k$ relevant career context chunks.
2. The retrieved context is strictly injected into the system prompt along with verified source citations:
   ```
   Context from O*NET / WEF Database:
   - Career: UX/UI Designer (Design & Creative Technologies)
   - Tasks: Design user flows, wireframes, conduct usability testing.
   - AI Impact: Wireframing augmented by Generative AI; human empathy and user research remain irreplaceable.
   - Sources: O*NET 15-1255.00, WEF Future of Jobs 2023.
   ```
3. The response generation adheres to the following instructions:
   - Cite authoritative sources in brackets (`[O*NET 2024]`, `[WEF 2023]`).
   - Use agency-preserving phrasing (*"Based on current trends, this option offers..."* rather than *"You must become..."*).
   - Provide concrete next actions and counterfactual exploration triggers.
