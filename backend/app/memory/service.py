# backend/app/memory/service.py
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.memory import StudentMemory
from app.models.research import ResearchEvent
from app.schemas.memory import JourneyResponse, JourneyTimelineEvent

class MemoryService:
    """
    Shared Persistence / Service Layer for Student Decision Memory.
    NOT an agent: provides stateful longitudinal context across all agents and sessions.
    """
    @staticmethod
    def log_event(db: Session, user_id: Optional[int], event_type: str, data: Dict[str, Any], session_id: Optional[str] = None):
        try:
            event = ResearchEvent(
                user_id=user_id,
                session_id=session_id,
                event_type=event_type,
                event_data=data,
                timestamp=datetime.now(timezone.utc)
            )
            db.add(event)
            db.commit()
        except Exception:
            try:
                db.rollback()
            except Exception:
                pass

    @staticmethod
    def record_explored_career(db: Session, user_id: int, career_id: str, career_name: str):
        existing = db.query(StudentMemory).filter(
            StudentMemory.user_id == user_id,
            StudentMemory.memory_type == "explored_career",
            StudentMemory.key == career_id
        ).first()
        
        now = datetime.now(timezone.utc)
        if not existing:
            mem = StudentMemory(
                user_id=user_id,
                memory_type="explored_career",
                key=career_id,
                value_json={"career_name": career_name, "visit_count": 1, "last_explored": now.isoformat()},
                created_at=now,
                updated_at=now
            )
            db.add(mem)
        else:
            val = dict(existing.value_json or {})
            val["visit_count"] = val.get("visit_count", 1) + 1
            val["last_explored"] = now.isoformat()
            existing.value_json = val
            existing.updated_at = now
            
        db.commit()
        MemoryService.log_event(db, user_id, "career_viewed", {"career_id": career_id, "career_name": career_name})

    @staticmethod
    def record_rejected_career(db: Session, user_id: int, career_id: str, career_name: str, reason: str):
        now = datetime.now(timezone.utc)
        mem = StudentMemory(
            user_id=user_id,
            memory_type="rejected_career",
            key=career_id,
            value_json={"career_name": career_name, "reason": reason, "rejected_at": now.isoformat()},
            created_at=now,
            updated_at=now
        )
        db.add(mem)
        db.commit()
        MemoryService.log_event(db, user_id, "career_rejected", {"career_id": career_id, "reason": reason})

    @staticmethod
    def toggle_saved_career(db: Session, user_id: int, career_id: str, career_name: str) -> bool:
        existing = db.query(StudentMemory).filter(
            StudentMemory.user_id == user_id,
            StudentMemory.memory_type == "saved_career",
            StudentMemory.key == career_id
        ).first()
        
        if existing:
            db.delete(existing)
            db.commit()
            MemoryService.log_event(db, user_id, "career_unsaved", {"career_id": career_id})
            return False
        else:
            now = datetime.now(timezone.utc)
            mem = StudentMemory(
                user_id=user_id,
                memory_type="saved_career",
                key=career_id,
                value_json={"career_name": career_name, "saved_at": now.isoformat()},
                created_at=now,
                updated_at=now
            )
            db.add(mem)
            db.commit()
            MemoryService.log_event(db, user_id, "career_saved", {"career_id": career_id})
            return True

    @staticmethod
    def record_what_if(db: Session, user_id: int, scenario_summary: str, details: Dict[str, Any]):
        now = datetime.now(timezone.utc)
        mem = StudentMemory(
            user_id=user_id,
            memory_type="what_if_scenario",
            key=f"what_if_{int(now.timestamp())}",
            value_json={"summary": scenario_summary, "details": details, "created_at": now.isoformat()},
            created_at=now,
            updated_at=now
        )
        db.add(mem)
        db.commit()
        MemoryService.log_event(db, user_id, "what_if_used", {"summary": scenario_summary})

    @staticmethod
    def get_student_memory_context(db: Session, user_id: int) -> str:
        """
        Retrieves condensed narrative context for agents & chatbot.
        """
        memories = db.query(StudentMemory).filter(StudentMemory.user_id == user_id).all()
        if not memories:
            return "New student session: No prior exploration trace recorded."

        explored = [m.value_json.get("career_name", m.key) for m in memories if m.memory_type == "explored_career"]
        saved = [m.value_json.get("career_name", m.key) for m in memories if m.memory_type == "saved_career"]
        rejected = [f"{m.value_json.get('career_name', m.key)} (Reason: {m.value_json.get('reason', 'N/A')})"
                    for m in memories if m.memory_type == "rejected_career"]
        what_ifs = [m.value_json.get("summary", "") for m in memories if m.memory_type == "what_if_scenario"]

        context_lines = []
        if explored:
            context_lines.append(f"Previously Explored Paths: {', '.join(explored[:5])}")
        if saved:
            context_lines.append(f"Bookmarked Shortlisted Careers: {', '.join(saved)}")
        if rejected:
            context_lines.append(f"Paths Explicitly Filtered Out: {'; '.join(rejected[:3])}")
        if what_ifs:
            context_lines.append(f"Recent Counterfactual Tests: {'; '.join(what_ifs[:3])}")

        return "\n".join(context_lines)

    @staticmethod
    def get_student_journey(db: Session, user_id: int) -> JourneyResponse:
        memories = db.query(StudentMemory).filter(StudentMemory.user_id == user_id).order_by(StudentMemory.created_at.desc()).all()
        
        explored = [m.value_json.get("career_name", m.key) for m in memories if m.memory_type == "explored_career"]
        saved = [m.value_json.get("career_name", m.key) for m in memories if m.memory_type == "saved_career"]
        rejected = [m.value_json for m in memories if m.memory_type == "rejected_career"]
        what_ifs = [m.value_json for m in memories if m.memory_type == "what_if_scenario"]
        
        timeline: List[JourneyTimelineEvent] = []
        for m in memories:
            timeline.append(JourneyTimelineEvent(
                timestamp=m.created_at,
                event_type=m.memory_type,
                title=f"{m.memory_type.replace('_', ' ').title()}: {m.key}",
                description=str(m.value_json.get("reason") or m.value_json.get("summary") or m.value_json.get("career_name") or ""),
                metadata=m.value_json or {}
            ))
            
        return JourneyResponse(
            total_careers_explored=len(explored),
            saved_careers=saved,
            rejected_careers_with_reasons=rejected,
            active_what_if_scenarios=what_ifs,
            learned_preferences={},
            timeline=timeline[:25]
        )

memory_service = MemoryService()
