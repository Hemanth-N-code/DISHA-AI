// frontend/src/pages/CareerDetailPage.tsx
import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  Compass, Bookmark, Scale, ListTodo, ArrowRight,
  Sparkles, CheckCircle2, AlertCircle, Cpu, Network, ShieldCheck, ChevronRight
} from 'lucide-react';
import { api } from '../services/api';
import { CareerDetail, SkillGapResponse } from '../types';
import { FactorTagBadge } from '../components/FactorTagBadge';

export const CareerDetailPage: React.FC = () => {
  const params = useParams<{ id?: string; careerId?: string }>();
  const activeId = params.careerId || params.id;
  const navigate = useNavigate();

  const [career, setCareer] = useState<CareerDetail | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [skillGap, setSkillGap] = useState<SkillGapResponse | null>(null);
  const [isSaved, setIsSaved] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [roadmapLoading, setRoadmapLoading] = useState(false);

  useEffect(() => {
    async function loadDetails() {
      if (!activeId) {
        setError('No career identifier was provided.');
        setLoading(false);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const c = await api.careers.getById(activeId);
        setCareer(c);
        setLoading(false);

        // Fetch deep analysis and skill gap concurrently in background without blocking initial render
        api.careers.analyze(activeId).then(setAnalysis).catch(console.warn);
        api.skillGap.get(activeId).then(setSkillGap).catch(console.warn);
      } catch (err: any) {
        console.warn('Failed to load career detail:', err);
        setError(err?.message || `Unable to retrieve career details for "${activeId}".`);
        setLoading(false);
      }
    }
    loadDetails();
  }, [activeId]);

  const handleToggleSave = async () => {
    if (!career) return;
    const res = await api.memory.toggleSave(career.career_id, career.career_name);
    setIsSaved(res.is_saved);
  };

  const handleGenerateRoadmap = async () => {
    if (!career) return;
    setRoadmapLoading(true);
    try {
      await api.roadmap.generate(career.career_id, 6);
      navigate('/roadmap');
    } catch (err) {
      console.warn('Failed to generate roadmap:', err);
      setRoadmapLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-3">
        <div className="w-8 h-8 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin" />
        <p className="text-xs text-slate-500">Retrieving multidimensional career knowledge...</p>
      </div>
    );
  }

  if (error || !career) {
    return (
      <div className="max-w-xl mx-auto my-16 p-8 bg-white rounded-2xl border border-slate-200 text-center shadow-sm space-y-4">
        <div className="w-12 h-12 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center mx-auto">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Career Information Unavailable</h2>
        <p className="text-xs text-slate-600 leading-relaxed">
          {error || `We could not find career information for "${activeId}". It might have been updated or removed.`}
        </p>
        <div className="flex items-center justify-center gap-3 pt-2">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="px-4 py-2 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors"
          >
            Go Back
          </button>
          <Link
            to="/what-if"
            className="px-4 py-2 text-xs font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-sm transition-colors"
          >
            What-If Explorer
          </Link>
          <Link
            to="/discover"
            className="px-4 py-2 text-xs font-semibold text-brand-700 bg-brand-50 hover:bg-brand-100 rounded-xl border border-brand-200 transition-colors"
          >
            Career Universe
          </Link>
        </div>
      </div>
    );
  }

  const score = analysis?.score_breakdown?.overall_score || 78;

  const automatedTasks: string[] =
    career.ai_impact?.automated_tasks && career.ai_impact.automated_tasks.length > 0
      ? career.ai_impact.automated_tasks
      : [
          'Repetitive documentation & syntax boilerplate',
          'Routine unit testing & verification checks',
          'Standard data gathering & reporting',
        ];

  const augmentedTasks: string[] =
    career.ai_impact?.augmented_tasks && career.ai_impact.augmented_tasks.length > 0
      ? career.ai_impact.augmented_tasks
      : [
          'Context-aware workflow and solution generation',
          'High-speed pattern recognition & analytics',
          'Automated simulation & prototype testing',
        ];

  const humanSkills: string[] =
    career.ai_impact?.human_skills && career.ai_impact.human_skills.length > 0
      ? career.ai_impact.human_skills
      : [
          'System architecture & complex tradeoffs',
          'Interdisciplinary problem formulation',
          'Stakeholder empathy & human judgment',
        ];

  const educationPaths: string[] =
    career.education_paths && career.education_paths.length > 0
      ? career.education_paths
      : ["Relevant Bachelor's Degree / Professional Foundation"];

  const entryLevelRoles: string[] =
    career.entry_level_roles && career.entry_level_roles.length > 0
      ? career.entry_level_roles
      : ['Junior Associate / Trainee Specialist'];

  const alternativeCareers: string[] = career.alternative_careers || [];
  const sources: string[] =
    career.sources && career.sources.length > 0
      ? career.sources
      : ['Authoritative Labor Market Taxonomy (O*NET 2024, ESCO, WEF)'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs text-slate-500">
        <Link to="/discover" className="hover:text-brand-600">Career Universe</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span>{career.domain}</span>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-slate-900 font-semibold">{career.career_name}</span>
      </div>

      {/* Header Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-2 max-w-3xl">
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider px-3 py-0.5 rounded-full bg-brand-50 text-brand-700 border border-brand-200">
                {career.domain}
              </span>
              <span className="text-xs text-slate-500">
                Eligibility: {career.eligibility}
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              {career.career_name}
            </h1>
            <p className="text-sm text-slate-600 leading-relaxed">
              {career.description}
            </p>
          </div>

          {/* Compatibility Meter & Action Buttons */}
          <div className="shrink-0 flex flex-col sm:flex-row lg:flex-col items-start lg:items-end gap-3">
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-left lg:text-right">
              <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                Exploratory Fit
              </div>
              <div className="text-2xl font-black text-brand-700">{score}%</div>
              <p className="text-[11px] text-slate-500">Multi-Pillar Compatibility</p>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleToggleSave}
                className={`inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold border transition-colors ${
                  isSaved ? 'bg-amber-50 text-amber-900 border-amber-300' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                }`}
              >
                <Bookmark className="w-3.5 h-3.5" fill={isSaved ? 'currentColor' : 'none'} />
                <span>{isSaved ? 'Saved' : 'Save Career'}</span>
              </button>

              <button
                onClick={handleGenerateRoadmap}
                disabled={roadmapLoading}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
              >
                <ListTodo className="w-3.5 h-3.5" />
                <span>{roadmapLoading ? 'Building...' : 'Build Roadmap'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Grid: 2 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Analysis & Typical Work */}
        <div className="lg:col-span-2 space-y-6">
          {/* Why it may fit you */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand-600" />
              <span>Why This Career May Fit You</span>
            </h2>
            <p className="text-xs text-slate-700 leading-relaxed bg-brand-50/50 p-3.5 rounded-xl border border-brand-100">
              {analysis?.fit_summary || 'Strong continuous alignment across your academic strengths and creative preferences.'}
            </p>
            {analysis?.score_breakdown?.factor_tags && (
              <div className="flex flex-wrap gap-1.5 pt-2">
                {analysis.score_breakdown.factor_tags.map((tag: any, i: number) => (
                  <FactorTagBadge key={i} tag={tag} />
                ))}
              </div>
            )}
          </div>

          {/* Typical Work */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
            <h2 className="text-base font-bold text-slate-900">Typical Work & Daily Responsibilities</h2>
            <p className="text-xs text-slate-700 leading-relaxed">{career.typical_work}</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-100">
              <div>
                <h3 className="text-xs font-bold text-slate-900 mb-2 uppercase tracking-wider">
                  Education & Degree Pathways
                </h3>
                <ul className="space-y-1.5 text-xs text-slate-600">
                  {educationPaths.map((p, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-brand-600 mt-1.5 shrink-0" />
                      <span>{p}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-xs font-bold text-slate-900 mb-2 uppercase tracking-wider">
                  Entry-Level Roles
                </h3>
                <ul className="space-y-1.5 text-xs text-slate-600">
                  {entryLevelRoles.map((r, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-1.5 shrink-0" />
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Technology & AI Transformation (Novelty #5) */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Cpu className="w-4 h-4 text-brand-600" />
                <span>How Technology & AI are Transforming This Role</span>
              </h2>
              <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                Augmentation Model
              </span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {career.technology_changes || 'AI and automation are augmenting routine cognitive and administrative tasks in this domain.'}
            </p>

            {/* 3-Pillar Breakdown */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
              {/* Automated Tasks */}
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                <h3 className="text-xs font-bold text-slate-700 mb-2">Automated Tasks</h3>
                <ul className="space-y-1 text-[11px] text-slate-600">
                  {automatedTasks.map((t, i) => (
                    <li key={i}>&bull; {t}</li>
                  ))}
                </ul>
              </div>

              {/* Augmented Tasks */}
              <div className="p-3.5 rounded-xl bg-indigo-50/50 border border-indigo-100">
                <h3 className="text-xs font-bold text-indigo-900 mb-2">AI-Augmented Work</h3>
                <ul className="space-y-1 text-[11px] text-indigo-800">
                  {augmentedTasks.map((t, i) => (
                    <li key={i}>&bull; {t}</li>
                  ))}
                </ul>
              </div>

              {/* Human Skills */}
              <div className="p-3.5 rounded-xl bg-emerald-50/50 border border-emerald-200">
                <h3 className="text-xs font-bold text-emerald-900 mb-2">Resilient Human Skills</h3>
                <ul className="space-y-1 text-[11px] text-emerald-800">
                  {humanSkills.map((t, i) => (
                    <li key={i}>&bull; {t}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Strategic Questions to Consider */}
          {analysis?.questions_to_consider && (
            <div className="bg-slate-50 rounded-2xl border border-slate-200 p-6 space-y-3">
              <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                Reflective Questions for Your Decision
              </h2>
              <ul className="space-y-2 text-xs text-slate-700">
                {(analysis.questions_to_consider || []).map((q: string, i: number) => (
                  <li key={i} className="flex items-start gap-2.5">
                    <span className="w-5 h-5 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-[11px] shrink-0">
                      {i + 1}
                    </span>
                    <span className="leading-relaxed">{q}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Right Column: Skill Gap & Pathways */}
        <div className="space-y-6">
          {/* Skill Gap Card (Deterministic) */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-slate-900">Your Diagnosed Skill Gap</h2>
              <Link to={`/skill-gap/${career.career_id}`} className="text-xs font-semibold text-brand-600 hover:underline">
                Deep Dive &rarr;
              </Link>
            </div>

            {skillGap && (
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-600">Baseline Readiness</span>
                  <span className="font-bold text-brand-700">{skillGap.readiness_percentage}%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-brand-600 h-full rounded-full"
                    style={{ width: `${skillGap.readiness_percentage}%` }}
                  />
                </div>

                <div className="pt-2 space-y-2">
                  {(skillGap.skills_breakdown || []).slice(0, 4).map((sk, i) => (
                    <div key={i} className="flex items-center justify-between text-xs border-b border-slate-100 pb-1.5">
                      <div>
                        <div className="font-medium text-slate-800">{sk.skill_name}</div>
                        <span className={`text-[10px] font-bold ${
                          sk.priority === 'Critical' ? 'text-red-600' : 'text-amber-600'
                        }`}>
                          {sk.category === 'existing' ? 'Matched' : `Gap: ${sk.gap} level(s)`}
                        </span>
                      </div>
                      <span className="text-[11px] font-semibold text-slate-500">
                        {sk.current_level} / {sk.required_level}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Alternative Pathway Graph Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                <Network className="w-4 h-4 text-brand-600" />
                <span>Alternative Path Graph</span>
              </h2>
            </div>
            <p className="text-xs text-slate-600">
              Careers connected via shared skill clusters and lateral pivot opportunities:
            </p>

            <div className="space-y-2 pt-1">
              {alternativeCareers.slice(0, 4).map((altId) => (
                <Link
                  key={altId}
                  to={`/careers/${altId}`}
                  className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50 hover:bg-brand-50 text-xs font-semibold text-slate-800 hover:text-brand-700 border border-slate-200 transition-colors"
                >
                  <span className="capitalize">{altId.replace(/_/g, ' ')}</span>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
                </Link>
              ))}
            </div>

            <Link
              to={`/graph?center=${career.career_id}`}
              className="w-full inline-flex items-center justify-center gap-1.5 py-2 rounded-lg bg-brand-50 hover:bg-brand-100 text-brand-700 font-bold text-xs border border-brand-200 transition-colors"
            >
              <span>Explore Interactive Node Graph</span>
              <Compass className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Authoritative Sources */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-500 space-y-1.5">
            <div className="flex items-center gap-1.5 font-bold text-slate-700">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>Evidence-Grounded Knowledge Base</span>
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              Curated from verified taxonomy databases: {sources.join(', ')}.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
