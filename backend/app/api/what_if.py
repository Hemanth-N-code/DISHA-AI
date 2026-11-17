# backend/app/api/what_if.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.profile import StudentProfile
from app.models.career import Career
from app.schemas.what_if import WhatIfRequest, WhatIfResponse
from app.api.deps import get_current_user
from app.recommendation.what_if import evaluate_what_if_scenario
from app.memory.service import memory_service

router = APIRouter(prefix="/what-if", tags=["What-If Counterfactuals"])

@router.post("", response_model=WhatIfResponse)
def run_what_if_simulation(
    req: WhatIfRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Student profile required for What-If scenario.")

    all_careers = db.query(Career).all()
    if not all_careers:
        raise HTTPException(status_code=500, detail="Career database empty.")

    # 1. Evaluate scenario
    res = evaluate_what_if_scenario(profile, all_careers, req)

    # 2. Record in memory
    memory_service.record_what_if(
        db=db,
        user_id=user.id,
        scenario_summary=res.scenario_description,
        details={
            "deltas_count": len(res.deltas),
            "cdi_shift": round(res.diversity_index_what_if - res.diversity_index_current, 3)
        }
    )

    # 3. If student explicitly asks to save this preference permanently:
    if req.save_as_permanent:
        if req.programming_preference is not None:
            profile.programming_preference = req.programming_preference
        if req.mathematics_preference is not None:
            profile.mathematics_preference = req.mathematics_preference
        if req.creativity_level is not None:
            profile.creativity_level = req.creativity_level
        if req.people_interaction_preference is not None:
            profile.people_interaction_preference = req.people_interaction_preference
        db.commit()

    return res
