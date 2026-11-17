# backend/app/rag/career_rag.py
from typing import List, Dict, Any, Optional
from app.rag.vector_store import vector_store
from app.services.llm_service import llm_service

def index_careers_for_rag(careers: List[Any]):
    """
    Chunks and indexes careers into the vector store.
    """
    documents = []
    for c in careers:
        career_id = getattr(c, "career_id", "")
        name = getattr(c, "career_name", "")
        domain = getattr(c, "domain", "")
        desc = getattr(c, "description", "")
        work = getattr(c, "typical_work", "")
        edu = ", ".join(getattr(c, "education_paths", []) or [])
        skills = ", ".join([s.get("skill", "") for s in (getattr(c, "required_skills", []) or [])])
        future = ", ".join(getattr(c, "future_skills", []) or [])
        changes = getattr(c, "technology_changes", "")
        sources = getattr(c, "sources", ["Authoritative National Taxonomy"])

        # Create structured text chunk
        content = (
            f"Career: {name} (ID: {career_id})\n"
            f"Domain: {domain}\n"
            f"Overview: {desc}\n"
            f"Typical Work & Daily Responsibilities: {work}\n"
            f"Education Paths: {edu}\n"
            f"Required Core Skills: {skills}\n"
            f"Future Resilient Skills: {future}\n"
            f"Technological Changes & AI Transformation: {changes}\n"
            f"Authoritative Sources: {', '.join(sources)}"
        )
        
        documents.append({
            "id": career_id,
            "content": content,
            "metadata": {
                "career_id": career_id,
                "career_name": name,
                "domain": domain,
                "sources": sources
            }
        })
        
    vector_store.add_documents(documents)

def answer_student_question_with_rag(
    query: str,
    career_context_id: Optional[str] = None,
    user_context_summary: Optional[str] = None,
    conversation_history: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    RAG Pipeline:
    Student Question -> Vector Search -> Relevant Career Context -> LLM -> Grounded Response
    """
    retrieved_docs = vector_store.similarity_search(query, top_k=3)
    
    # If specific career context is active, prioritize that career
    primary_doc = None
    if career_context_id:
        for doc in vector_store.documents:
            if doc.get("metadata", {}).get("career_id") == career_context_id:
                primary_doc = doc
                break

    context_snippets = []
    sources = []
    
    if primary_doc:
        context_snippets.append(primary_doc["content"])
        sources.extend(primary_doc.get("metadata", {}).get("sources", []))
        
    for r in retrieved_docs:
        if primary_doc and r["id"] == primary_doc["id"]:
            continue
        context_snippets.append(r["content"])
        sources.extend(r.get("metadata", {}).get("sources", []))

    assembled_context = "\n---\n".join(context_snippets[:3])
    
    system_prompt = (
        "You are DISHA AI, an evidence-grounded Career Decision-Exploration Assistant. "
        "Your mission is to help students explore, compare, and understand career directions without dictating rigid outcomes. "
        "Always ground your responses in verified career knowledge. Never make false promises or use authoritarian language like 'You must become X'. "
        "Use supportive, exploratory phrasing like 'This pathway offers...', 'Potential fits to consider include...'"
    )
    
    full_prompt = query
    if user_context_summary:
        full_prompt = f"Student Profile Context: {user_context_summary}\n\nQuestion: {query}"
        
    reply = llm_service.generate_completion(
        prompt=full_prompt,
        system_prompt=system_prompt,
        context=assembled_context,
        max_tokens=850,
        query_only=query,
        conversation_history=conversation_history
    )
    
    unique_sources = list(dict.fromkeys(sources))[:3]
    if not unique_sources:
        unique_sources = ["Bureau of Labor Statistics (BLS)", "IEEE Career Taxonomy", "O*NET Guidelines"]

    # Detect if user query implies a what-if trigger
    what_if_trigger = None
    q_lower = query.lower()
    if "what if" in q_lower or "less coding" in q_lower or "don't want coding" in q_lower or "more math" in q_lower:
        what_if_trigger = {
            "query": query,
            "suggested_action": "Open What-If Explorer to recalculate compatibility scores dynamically"
        }

    return {
        "reply": reply,
        "grounded_career_sources": unique_sources,
        "retrieved_context_count": len(context_snippets),
        "what_if_trigger": what_if_trigger
    }
