# backend/app/api/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.profile import StudentProfile
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.deps import get_current_user_optional
from app.rag.career_rag import answer_student_question_with_rag
from app.services.llm_service import llm_service
from app.memory.service import memory_service

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Conversational AI Counselor"])

@router.post("", response_model=ChatResponse)
def chat_with_assistant(
    req: ChatRequest,
    user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    try:
        profile_summary = None
        memory_context = ""

        if user:
            try:
                profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
                if profile:
                    profile_summary = f"{profile.stream} stream, interested in {', '.join(profile.interests or [])}, prefers {profile.programming_preference} programming."
                memory_context = memory_service.get_student_memory_context(db, user.id)
            except Exception as e:
                logger.warning(f"Could not load student profile/memory trace: {e}")
            finally:
                try:
                    db.rollback()  # Instantly release any SQLite shared read locks
                except Exception:
                    pass

        combined_context = f"{profile_summary or ''}\nMemory Trace:\n{memory_context}".strip()

        rag_res = answer_student_question_with_rag(
            query=req.message,
            career_context_id=req.career_context_id,
            user_context_summary=combined_context,
            conversation_history=req.conversation_history
        )

        # Dynamic suggestions
        suggestions = [
            "What adjacent careers exist for this path?",
            "How will AI change the daily tasks of this job?",
            "Show my deterministic skill gap for this career"
        ]
        if "programming" in req.message.lower():
            suggestions.append("Test 'What if I want less programming?' in What-If Explorer")

        return ChatResponse(
            reply=rag_res.get("reply", "I am analyzing your career query. Please explore specific engineering branches or cutoffs."),
            suggested_actions=suggestions,
            grounded_career_sources=rag_res.get("grounded_career_sources", ["Bureau of Labor Statistics (BLS)", "IEEE Career Taxonomy", "O*NET Guidelines"]),
            what_if_trigger=rag_res.get("what_if_trigger")
        )
    except Exception as exc:
        logger.exception("Unexpected error in chat_with_assistant: %s", exc)
        # Return graceful grounded guidance instead of 500 error
        fallback_reply = llm_service._generate_offline_grounded_response(
            prompt=req.message,
            query_only=req.message,
            conversation_history=req.conversation_history
        )
        return ChatResponse(
            reply=fallback_reply,
            suggested_actions=[
                "Compare branches in What-If Explorer",
                "Check KCET cutoffs for 58 Karnataka colleges",
                "Explore 118 grounded career profiles"
            ],
            grounded_career_sources=["O*NET 2024 Content Model", "WEF Future of Jobs 2023", "Karnataka Examination Authority (KEA)"]
        )
