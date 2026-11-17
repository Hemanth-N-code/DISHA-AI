// frontend/src/types/index.ts

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
}

export interface SkillItem {
  skill: string;
  level: number; // 1 to 5
}

export interface StudentProfile {
  id: number;
  user_id: number;
  education_level: string;
  stream: string;
  subjects: string[];
  marks_percentage: number;
  favorite_subjects: string[];
  interests: string[];
  skills: SkillItem[];
  preferences: string[];
  goals: string[];
  constraints: string[];
  programming_preference: 'none' | 'low' | 'moderate' | 'high';
  mathematics_preference: 'low' | 'moderate' | 'high';
  creativity_level: 'low' | 'moderate' | 'high';
  people_interaction_preference: 'low' | 'balanced' | 'high';
  profile_summary?: string;
  academic_strengths?: string[];
}

export interface FactorTag {
  positive: boolean;
  text: string;
}

export interface ScoreBreakdown {
  overall_score: number;
  interest_fit: number;
  academic_fit: number;
  skill_fit: number;
  preference_fit: number;
  goal_fit: number;
  factor_tags: FactorTag[];
  explanation: string;
}

export interface CareerCandidate {
  career_id: string;
  career_name: string;
  domain: string;
  description: string;
  typical_work: string;
  eligibility: string;
  score_breakdown: ScoreBreakdown;
  is_diversity_highlight: boolean;
  diversity_domain: string;
}

export interface AIImpact {
  automated_tasks: string[];
  augmented_tasks: string[];
  human_skills: string[];
}

export interface CareerDetail {
  id: number;
  career_id: string;
  career_name: string;
  domain: string;
  description: string;
  typical_work: string;
  education_paths: string[];
  eligibility: string;
  required_skills: { skill: string; level: number; importance: string }[];
  soft_skills: string[];
  related_careers: string[];
  alternative_careers: string[];
  adjacent_careers: string[];
  entry_level_roles: string[];
  higher_study_options: string[];
  certifications: string[];
  projects: string[];
  portfolio_requirements: string[];
  internship_options: string[];
  future_skills: string[];
  technology_changes?: string;
  ai_impact: AIImpact;
  pathway?: string;
  sources: string[];
}

export interface SkillGapItem {
  skill_name: string;
  current_level: number;
  required_level: number;
  gap: number;
  category: 'existing' | 'partially_developed' | 'missing';
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  recommended_action: string;
}

export interface SkillGapResponse {
  career_id: string;
  career_name: string;
  total_skills_evaluated: number;
  matched_skills_count: number;
  gap_skills_count: number;
  readiness_percentage: number;
  skills_breakdown: SkillGapItem[];
  top_priority_focus_areas: string[];
  estimated_upskilling_months: number;
}

export interface ScenarioDelta {
  career_id: string;
  career_name: string;
  domain: string;
  previous_score: number;
  new_score: number;
  score_change: number;
  status: 'surged' | 'declined' | 'newly_unlocked' | 'stable';
  reason: string;
}

export interface WhatIfResponse {
  scenario_description: string;
  current_top_careers: CareerCandidate[];
  what_if_top_careers: CareerCandidate[];
  deltas: ScenarioDelta[];
  explanation: string;
  diversity_index_current: number;
  diversity_index_what_if: number;
}

export interface CareerComparisonItem {
  career_id: string;
  career_name: string;
  domain: string;
  description: string;
  education_duration: string;
  typical_work: string;
  score_breakdown: ScoreBreakdown;
  key_skills_required: string[];
  missing_skills_count: number;
  future_readiness_score: number;
  work_characteristics: Record<string, string>;
  learning_curve_complexity: string;
  sample_entry_role: string;
}

export interface CompareResponse {
  compared_careers: CareerComparisonItem[];
  neutral_observations: string[];
  tradeoff_insights: Record<string, string>;
}

export interface RoadmapTask {
  id: number;
  roadmap_id: number;
  title: string;
  description: string;
  category: string;
  stage_index: number;
  estimated_weeks: number;
  status: 'not_started' | 'in_progress' | 'completed';
  portfolio_artifact?: string;
  completed_at?: string;
}

export interface Roadmap {
  id: number;
  user_id: number;
  career_id: string;
  career_name: string;
  target_horizon_months: number;
  overall_progress: number;
  created_at: string;
  tasks: RoadmapTask[];
}

export interface JourneyTimelineEvent {
  timestamp: string;
  event_type: string;
  title: string;
  description: string;
  metadata: Record<string, any>;
}

export interface JourneyResponse {
  total_careers_explored: number;
  saved_careers: string[];
  rejected_careers_with_reasons: { career_name: string; reason: string; rejected_at: string }[];
  active_what_if_scenarios: any[];
  learned_preferences: Record<string, any>;
  timeline: JourneyTimelineEvent[];
}

export interface ResearchMetrics {
  total_students: number;
  total_explorations: number;
  total_comparisons: number;
  total_what_if_queries: number;
  total_roadmaps_created: number;
  average_career_diversity_index: number;
  average_pre_confidence: number;
  average_post_confidence: number;
  confidence_delta: number;
  domain_coverage_distribution: Record<string, number>;
  top_counterfactual_shifts: { shift: string; unlocked_domain: string; surge_percentage: string }[];
  recent_events_sample: { event_type: string; data: any; timestamp: string }[];
}

// CET Support Module Types
export interface CetExam {
  id: string;
  name: string;
  authority: string;
  state: string;
  is_active: boolean;
}

export interface CetDomain {
  id: string;
  exam_id: string;
  name: string;
  course_group: string;
  is_active: boolean;
}

export interface CollegePlacement {
  year: number;
  placement_rate?: number;
  median_package_lpa?: number;
  average_package_lpa?: number;
  highest_package_lpa?: number;
  top_recruiters: string[];
  source: string;
  is_official: boolean;
}

export interface CollegeBranch {
  id: number;
  course_id: string;
  branch_name: string;
  branch_code: string;
  intake: number;
  tuition_fee_annual?: number;
}

export interface CollegeDetail {
  id: string;
  code: string;
  name: string;
  short_name: string;
  location: string;
  city: string;
  district: string;
  college_type: string;
  website?: string;
  established_year?: number;
  accreditation?: string;
  campus_area_acres?: number;
  hostel_facility: boolean;
  description?: string;
  source: string;
  source_url?: string;
  branches: CollegeBranch[];
  placement?: CollegePlacement;
}

export interface StudentCetProfile {
  id: number;
  user_id: number;
  exam_id: string;
  domain_id: string;
  rank: number;
  category: string;
  sub_category?: string;
  gender: string;
  preferred_branches: string[];
  preferred_locations: string[];
  preferences: string[];
  updated_at: string;
}

export interface CetOptionMatchItem {
  college_id: string;
  college_code: string;
  college_name: string;
  college_short_name: string;
  city: string;
  college_type: string;
  branch_id: number;
  branch_name: string;
  branch_code: string;
  tuition_fee_annual?: number;
  historical_match_label: string;
  match_badge_color: string;
  historical_explanation: string;
  match_score: number;
  closing_ranks: Record<number, number>;
  most_recent_closing_rank?: number;
  placement?: {
    median_package_lpa?: number;
    highest_package_lpa?: number;
    top_recruiters?: string[];
    placement_rate?: number;
    source?: string;
  };
  source: string;
  source_url?: string;
}

export interface CetAnalyzeResponse {
  student_rank: number;
  category: string;
  round_num: number;
  total_options_evaluated: number;
  strong_matches_count: number;
  possible_matches_count: number;
  safer_matches_count: number;
  competitive_matches_count: number;
  options: CetOptionMatchItem[];
  disclaimer: string;
}

export interface CutoffTrendPoint {
  year: number;
  round: number;
  closing_rank: number;
  category: string;
}

export interface CutoffTrendResponse {
  college_id: string;
  branch_code: string;
  category: string;
  round: number;
  trend_points: CutoffTrendPoint[];
  direction: string;
  available_years: number[];
}

export interface CollegeCompareItem {
  college_id: string;
  code: string;
  name: string;
  short_name: string;
  city: string;
  college_type: string;
  branch_name: string;
  branch_code: string;
  tuition_fee_annual?: number;
  cutoffs_by_year: Record<number, number>;
  placement?: {
    median_package_lpa?: number;
    average_package_lpa?: number;
    highest_package_lpa?: number;
    top_recruiters: string[];
    placement_rate?: number;
    source: string;
  };
  campus_area_acres?: number;
  hostel_facility: boolean;
  accreditation?: string;
  source: string;
}

export interface CollegeComparisonResponse {
  branch_code: string;
  category: string;
  colleges: CollegeCompareItem[];
  disclaimer: string;
}

export interface OptionItem {
  id: number;
  option_list_id: number;
  college_branch_id: number;
  priority_order: number;
  historical_category: string;
  student_notes?: string;
  college_name: string;
  college_short_name: string;
  branch_name: string;
  branch_code: string;
  city: string;
}

export interface OptionListResponse {
  id: number;
  user_id: number;
  title: string;
  notes?: string;
  items: OptionItem[];
  disclaimer: string;
}

export interface CareerBranchMappingResponse {
  career_id: string;
  career_name: string;
  recommended_branches: string[];
  rationale: string;
}

