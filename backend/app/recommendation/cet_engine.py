# backend/app/recommendation/cet_engine.py
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.cet import (
    College, CollegeBranch, HistoricalCutoff, CollegePlacement,
    StudentCetProfile, Course, Exam, CetDomain
)

def classify_historical_match(student_rank: int, closing_ranks: List[int]) -> Tuple[str, str, str]:
    """
    Classifies student rank against historical closing ranks without predicting or guaranteeing admission.
    Returns (category_label, badge_color, human_explanation)
    """
    if not closing_ranks:
        return (
            "Insufficient historical evidence",
            "gray",
            "Historical closing cutoff records are unavailable for this specific category and branch combination."
        )

    recent_closing = closing_ranks[0] # most recent year (e.g. 2025 or 2024)
    avg_closing = sum(closing_ranks) / len(closing_ranks)

    # Years where student rank was within closing rank
    years_within = sum(1 for c in closing_ranks if student_rank <= c)
    total_years = len(closing_ranks)

    # Safe boundary: student rank significantly below closing rank (<= 0.75 * closing)
    if student_rank <= recent_closing * 0.75:
        return (
            "Lower historical cutoff / safer option",
            "purple",
            f"Your rank ({student_rank:,}) was comfortably within the historical closing ranks in {years_within} of the last {total_years} evaluated year(s) (recent cutoff: {recent_closing:,}). Provides a solid safety cushion."
        )
    elif student_rank <= recent_closing * 0.98:
        return (
            "Strong historical match",
            "green",
            f"Your rank ({student_rank:,}) is within the historical closing cutoff range ({recent_closing:,}) in {years_within} of the last {total_years} recorded year(s)."
        )
    elif student_rank <= recent_closing * 1.15:
        return (
            "Possible match",
            "blue",
            f"Your rank ({student_rank:,}) is close to recent historical closing marks ({recent_closing:,}). Variations in seat matrix or applicant choices will determine allotment."
        )
    else:
        return (
            "Competitive option",
            "amber",
            f"Your rank ({student_rank:,}) is above recent historical closing marks ({recent_closing:,}). This represents an ambitious / aspirational choice."
        )

def get_cutoff_trend(
    db: Session,
    college_id: str,
    branch_code: str,
    category: str = "GM",
    round_num: int = 1
) -> Dict[str, Any]:
    """
    Retrieves multi-year closing ranks for a specific college, branch, category, and round.
    """
    cutoffs = db.query(HistoricalCutoff).filter(
        HistoricalCutoff.college_id == college_id,
        HistoricalCutoff.branch_code == branch_code,
        HistoricalCutoff.category == category,
        HistoricalCutoff.round == round_num
    ).order_by(HistoricalCutoff.year.asc()).all()

    trend_points = []
    closing_ranks = []
    for c in cutoffs:
        trend_points.append({
            "year": c.year,
            "closing_rank": c.closing_rank,
            "opening_rank": c.opening_rank,
            "source": c.source
        })
        closing_ranks.append(c.closing_rank)

    # Determine trend direction (tightening, widening, stable)
    direction = "Stable"
    if len(closing_ranks) >= 2:
        diff = closing_ranks[-1] - closing_ranks[0]
        if diff < -500:
            direction = "Cutoff Tightening (More Competitive)"
        elif diff > 500:
            direction = "Cutoff Widening (Less Competitive)"

    return {
        "college_id": college_id,
        "branch_code": branch_code,
        "category": category,
        "round": round_num,
        "trend_points": trend_points,
        "direction": direction,
        "available_years": [p["year"] for p in trend_points]
    }

def analyze_student_options(
    db: Session,
    rank: int,
    category: str = "GM",
    domain_id: str = "engineering",
    preferred_branches: Optional[List[str]] = None,
    preferred_locations: Optional[List[str]] = None,
    preferences: Optional[List[str]] = None,
    round_num: int = 1,
    sort_by: Optional[str] = "match_score"
) -> List[Dict[str, Any]]:
    """
    Generates tailored college + branch combinations with historical match classification,
    placement indicators, and multi-year cutoff trends.
    """
    branches_query = db.query(CollegeBranch).join(College).filter(
        CollegeBranch.is_active == True
    )

    if preferred_branches:
        branches_query = branches_query.filter(CollegeBranch.branch_code.in_(preferred_branches))

    if preferred_locations and "Any" not in preferred_locations:
        branches_query = branches_query.filter(College.city.in_(preferred_locations))

    branches = branches_query.all()
    results = []

    for b in branches:
        college = b.college

        # Fetch historical cutoffs across 2025, 2024, 2023 for this branch and category
        cutoffs = db.query(HistoricalCutoff).filter(
            HistoricalCutoff.college_id == college.id,
            HistoricalCutoff.branch_code == b.branch_code,
            HistoricalCutoff.category == category,
            HistoricalCutoff.round == round_num
        ).order_by(HistoricalCutoff.year.desc()).all()

        closing_ranks_by_year = {c.year: c.closing_rank for c in cutoffs}
        sorted_closings = [c.closing_rank for c in cutoffs]

        match_label, badge_color, explanation = classify_historical_match(rank, sorted_closings)

        # Placement information
        placement = db.query(CollegePlacement).filter(
            CollegePlacement.college_id == college.id
        ).order_by(CollegePlacement.year.desc()).first()

        placement_summary = None
        if placement:
            placement_summary = {
                "placement_rate": placement.placement_rate,
                "median_package_lpa": placement.median_package_lpa,
                "average_package_lpa": placement.average_package_lpa,
                "highest_package_lpa": placement.highest_package_lpa,
                "top_recruiters": placement.top_recruiters[:4] if placement.top_recruiters else [],
                "source": placement.source,
                "is_official": placement.is_official
            }

        # Calculate a transparent multidimensional match score (0-100)
        # 1. Historical Rank Fit (40%)
        # 2. Branch Preference (25%)
        # 3. Location Preference (20%)
        # 4. Placement Indicator (15%)
        rank_fit_score = 50.0
        if sorted_closings:
            recent = sorted_closings[0]
            if rank <= recent * 0.8:
                rank_fit_score = 95.0
            elif rank <= recent:
                rank_fit_score = 85.0
            elif rank <= recent * 1.15:
                rank_fit_score = 65.0
            else:
                rank_fit_score = 35.0

        branch_fit_score = 90.0 if preferred_branches and b.branch_code in preferred_branches else 60.0
        location_fit_score = 95.0 if preferred_locations and (college.city in preferred_locations or "Any" in preferred_locations) else 50.0
        placement_fit_score = (placement.placement_rate if placement and placement.placement_rate else 75.0)

        overall_score = round(
            (0.40 * rank_fit_score) +
            (0.25 * branch_fit_score) +
            (0.20 * location_fit_score) +
            (0.15 * placement_fit_score),
            1
        )

        results.append({
            "college_id": college.id,
            "college_code": college.code,
            "college_name": college.name,
            "college_short_name": college.short_name,
            "city": college.city,
            "college_type": college.college_type,
            "branch_id": b.id,
            "branch_name": b.branch_name,
            "branch_code": b.branch_code,
            "tuition_fee_annual": b.tuition_fee_annual,
            "historical_match_label": match_label,
            "match_badge_color": badge_color,
            "historical_explanation": explanation,
            "match_score": overall_score,
            "closing_ranks": closing_ranks_by_year,
            "most_recent_closing_rank": sorted_closings[0] if sorted_closings else None,
            "placement": placement_summary,
            "source": cutoffs[0].source if cutoffs else "KEA Official Reports",
            "source_url": cutoffs[0].source_url if cutoffs else "https://cetonline.karnataka.gov.in/kea/"
        })

    # Sort results according to requested vision criteria
    if sort_by == "placement_desc":
        results.sort(key=lambda x: (
            -(x["placement"]["median_package_lpa"] if x.get("placement") and x["placement"].get("median_package_lpa") else 0),
            -x["match_score"]
        ))
    elif sort_by == "cutoff_asc":
        results.sort(key=lambda x: (x["most_recent_closing_rank"] or 999999, -x["match_score"]))
    elif sort_by == "cutoff_desc":
        results.sort(key=lambda x: (-(x["most_recent_closing_rank"] or 0), -x["match_score"]))
    else:
        # Default: prioritize Strong/Possible/Safer matches, then match score
        match_priority = {
            "Strong historical match": 1,
            "Possible match": 2,
            "Lower historical cutoff / safer option": 3,
            "Competitive option": 4,
            "Insufficient historical evidence": 5
        }
        results.sort(key=lambda x: (match_priority.get(x["historical_match_label"], 99), -x["match_score"]))

    return results

def compare_colleges(
    db: Session,
    college_ids: List[str],
    branch_code: str = "CS",
    category: str = "GM"
) -> Dict[str, Any]:
    """
    Conducts multidimensional side-by-side comparison across 2-4 colleges for a specific branch.
    """
    colleges = db.query(College).filter(College.id.in_(college_ids)).all()
    comparison_items = []

    for col in colleges:
        # Get branch
        branch = db.query(CollegeBranch).filter(
            CollegeBranch.college_id == col.id,
            CollegeBranch.branch_code == branch_code
        ).first()

        # Get historical cutoffs
        cutoffs = db.query(HistoricalCutoff).filter(
            HistoricalCutoff.college_id == col.id,
            HistoricalCutoff.branch_code == branch_code,
            HistoricalCutoff.category == category,
            HistoricalCutoff.round == 1
        ).order_by(HistoricalCutoff.year.desc()).all()

        closing_ranks = {c.year: c.closing_rank for c in cutoffs}

        # Get placement
        placement = db.query(CollegePlacement).filter(
            CollegePlacement.college_id == col.id
        ).order_by(CollegePlacement.year.desc()).first()

        comparison_items.append({
            "college_id": col.id,
            "college_code": col.code,
            "name": col.name,
            "short_name": col.short_name,
            "location": col.location,
            "city": col.city,
            "college_type": col.college_type,
            "established_year": col.established_year,
            "accreditation": col.accreditation,
            "hostel_facility": col.hostel_facility,
            "campus_area_acres": col.campus_area_acres,
            "website": col.website,
            "branch_name": branch.branch_name if branch else branch_code,
            "branch_code": branch_code,
            "tuition_fee_annual": branch.tuition_fee_annual if branch else None,
            "closing_ranks": closing_ranks,
            "placement": {
                "placement_rate": placement.placement_rate if placement else None,
                "median_package_lpa": placement.median_package_lpa if placement else None,
                "average_package_lpa": placement.average_package_lpa if placement else None,
                "highest_package_lpa": placement.highest_package_lpa if placement else None,
                "top_recruiters": placement.top_recruiters if placement else [],
                "source": placement.source if placement else "Not available",
                "is_official": placement.is_official if placement else False
            } if placement else None
        })

    return {
        "compared_colleges": comparison_items,
        "branch_code": branch_code,
        "category": category,
        "disclaimer": "Historical cutoff data is indicative only. Actual allotment depends on the current year's cutoff, seat availability, category, course, round, reservation and KEA counselling rules."
    }

def map_career_to_cet_branches(career_id: str) -> List[Dict[str, str]]:
    """
    Connects DISHA's 118 career recommendations directly to relevant CET academic branches.
    """
    mapping = {
        # Tech & Computing
        "data_scientist": [
            {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Direct Prerequisite"},
            {"branch_code": "AI", "branch_name": "Artificial Intelligence & Machine Learning", "relevance": "Direct Specialization"},
            {"branch_code": "DS", "branch_name": "Data Science & Engineering", "relevance": "Direct Specialization"}
        ],
        "ai_engineer": [
            {"branch_code": "AI", "branch_name": "Artificial Intelligence & Machine Learning", "relevance": "Direct Specialization"},
            {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Core Foundation"},
            {"branch_code": "EC", "branch_name": "Electronics & Communication Engineering", "relevance": "Hardware & Embedded AI"}
        ],
        "software_engineer": [
            {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Direct Prerequisite"},
            {"branch_code": "IS", "branch_name": "Information Science & Engineering", "relevance": "Direct Prerequisite"}
        ],
        "ux_designer": [
            {"branch_code": "IS", "branch_name": "Information Science & Engineering", "relevance": "HCI & Software Design"},
            {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Front-End & Product Architecture"}
        ],
        "cloud_architect": [
            {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Systems & Networks"},
            {"branch_code": "IS", "branch_name": "Information Science & Engineering", "relevance": "Enterprise Systems"}
        ],
        "robotics_engineer": [
            {"branch_code": "EC", "branch_name": "Electronics & Communication Engineering", "relevance": "Control Systems & Sensors"},
            {"branch_code": "ME", "branch_name": "Mechanical Engineering", "relevance": "Kinematics & Dynamics"},
            {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Robotics Software & Vision"}
        ],
        "iot_specialist": [
            {"branch_code": "EC", "branch_name": "Electronics & Communication Engineering", "relevance": "Sensors & Wireless"},
            {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Embedded Software"}
        ]
    }

    return mapping.get(career_id, [
        {"branch_code": "CS", "branch_name": "Computer Science & Engineering", "relevance": "Recommended Engineering Foundation"},
        {"branch_code": "EC", "branch_name": "Electronics & Communication Engineering", "relevance": "Core Technical Foundation"}
    ])
