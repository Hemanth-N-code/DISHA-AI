// frontend/src/pages/CareerComparisonPage.tsx
import React, { useState, useEffect } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import {
  Scale, Plus, X, ArrowUpRight, Compass, ShieldCheck, CheckCircle2,
  AlertCircle, Sparkles, BookOpen, Clock, Activity, Cpu, Briefcase
} from 'lucide-react';
import { api } from '../services/api';
import { CompareResponse, CareerDetail, CareerComparisonItem } from '../types';

export const CareerComparisonPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const [careerCatalog, setCareerCatalog] = useState<CareerDetail[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [comparison, setComparison] = useState<CompareResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [addDropdownVal, setAddDropdownVal] = useState<string>('');

  // Initial parse of URL params
  useEffect(() => {
    const idsParam = searchParams.get('careers');
    if (idsParam) {
      const parsed = idsParam.split(',').filter(Boolean);
      setSelectedIds(parsed);
    } else {
      // Default demo comparison: UX Designer vs Data Scientist
      setSelectedIds(['ux_designer', 'data_scientist']);
    }
  }, [searchParams]);

  // Load catalog for the Add Career dropdown
  useEffect(() => {
    api.careers.list().then((list) => setCareerCatalog(list)).catch(console.warn);
  }, []);

  // Fetch comparison whenever selectedIds change
  useEffect(() => {
    if (selectedIds.length < 2) {
      setLoading(false);
      setComparison(null);
      return;
    }

    setLoading(true);
    api.careers.compare(selectedIds)
      .then((res) => {
        setComparison(res);
      })
      .catch((err) => {
        console.warn('Comparison failed:', err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [selectedIds]);

  const handleRemoveCareer = (id: string) => {
    if (selectedIds.length <= 2) {
      alert('Comparison requires at least 2 careers.');
      return;
    }
    const updated = selectedIds.filter((cid) => cid !== id);
    setSelectedIds(updated);
    setSearchParams({ careers: updated.join(',') });
  };

  const handleAddCareer = (id: string) => {
    if (!id || selectedIds.includes(id)) return;
    if (selectedIds.length >= 4) {
      alert('You can compare up to 4 careers simultaneously.');
      return;
    }
    const updated = [...selectedIds, id];
    setSelectedIds(updated);
    setSearchParams({ careers: updated.join(',') });
    setAddDropdownVal('');
  };

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs px-3 py-1 rounded-full bg-brand-50 text-brand-700 font-semibold border border-brand-200 uppercase tracking-wider">
                  Novelty #1: Multi-Dimensional Tradeoff Evaluation
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
                <Scale className="w-7 h-7 text-brand-600" />
                Career Trade-Off Comparator
              </h1>
              <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-3xl">
                Compare up to 4 distinct careers side-by-side across 10 empirical dimensions. DISHA intentionally presents neutral trade-offs rather than forcing a single winner, preserving your personal decision agency.
              </p>
            </div>

            {/* Add Career Dropdown */}
            <div className="flex items-center gap-2">
              <select
                value={addDropdownVal}
                onChange={(e) => handleAddCareer(e.target.value)}
                className="text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
              >
                <option value="">+ Add Career to Compare...</option>
                {careerCatalog
                  .filter((c) => !selectedIds.includes(c.career_id))
                  .map((c) => (
                    <option key={c.career_id} value={c.career_id}>
                      {c.career_name} ({c.domain})
                    </option>
                  ))}
              </select>
            </div>
          </div>
        </div>

        {/* Neutral Observations Callout */}
        {comparison && comparison.neutral_observations.length > 0 && (
          <div className="bg-gradient-to-r from-brand-900 to-indigo-900 rounded-2xl p-6 text-white shadow-md space-y-3">
            <div className="flex items-center gap-2 text-brand-300 text-xs font-bold uppercase tracking-wider">
              <Compass className="w-4 h-4" /> Balanced Decision Guidance
            </div>
            <div className="space-y-1.5">
              {comparison.neutral_observations.map((obs, idx) => (
                <p key={idx} className="text-sm text-brand-100 flex items-start gap-2">
                  <span className="text-brand-400 font-bold">•</span>
                  <span>{obs}</span>
                </p>
              ))}
            </div>
          </div>
        )}

        {/* Main Comparison Matrix */}
        {loading ? (
          <div className="bg-white border border-slate-200 rounded-2xl p-16 text-center shadow-sm">
            <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium text-slate-700">Synthesizing multi-dimensional comparison metrics...</p>
          </div>
        ) : comparison && comparison.compared_careers.length > 0 ? (
          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/70">
                    <th className="p-4 sm:p-5 w-48 text-xs font-bold text-slate-500 uppercase tracking-wider">
                      Evaluation Dimension
                    </th>
                    {comparison.compared_careers.map((career) => (
                      <th
                        key={career.career_id}
                        className="p-4 sm:p-5 min-w-[240px] max-w-[320px] align-top relative"
                      >
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-brand-50 text-brand-700 border border-brand-200 uppercase tracking-wider">
                              {career.domain}
                            </span>
                            <h3 className="text-base font-bold text-slate-900 mt-1">
                              {career.career_name}
                            </h3>
                          </div>
                          {comparison.compared_careers.length > 2 && (
                            <button
                              type="button"
                              onClick={() => handleRemoveCareer(career.career_id)}
                              className="text-slate-400 hover:text-rose-600 p-1 rounded-lg hover:bg-slate-100 transition-colors"
                              title="Remove from comparison"
                            >
                              <X className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-100 text-sm">
                  {/* Row 1: Overall Compatibility */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      Overall Compatibility
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5">
                        <div className="flex items-center gap-3">
                          <span className="text-2xl font-black text-brand-600">
                            {c.score_breakdown.overall_score}%
                          </span>
                          <div className="text-xs text-slate-500">
                            Pillar fit score
                          </div>
                        </div>
                        <div className="w-full bg-slate-100 h-2 rounded-full mt-2 overflow-hidden">
                          <div
                            className="bg-brand-600 h-full rounded-full"
                            style={{ width: `${c.score_breakdown.overall_score}%` }}
                          />
                        </div>
                      </td>
                    ))}
                  </tr>

                  {/* Row 2: 5-Pillar Score Breakdown */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      5-Pillar Fit Breakdown
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs space-y-1.5 text-slate-600">
                        <div className="flex justify-between">
                          <span>Interest Alignment:</span>
                          <span className="font-semibold text-slate-800">{c.score_breakdown.interest_fit}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Academic Eligibility:</span>
                          <span className="font-semibold text-slate-800">{c.score_breakdown.academic_fit}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Skill Readiness:</span>
                          <span className="font-semibold text-slate-800">{c.score_breakdown.skill_fit}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Preference Match:</span>
                          <span className="font-semibold text-slate-800">{c.score_breakdown.preference_fit}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Goal Alignment:</span>
                          <span className="font-semibold text-slate-800">{c.score_breakdown.goal_fit}%</span>
                        </div>
                      </td>
                    ))}
                  </tr>

                  {/* Row 3: Educational Duration & Path */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        Education & Commitment
                      </div>
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs text-slate-700">
                        <div className="font-semibold text-slate-900 mb-1">{c.education_duration}</div>
                        <div className="text-slate-500">{c.work_characteristics.eligibility}</div>
                      </td>
                    ))}
                  </tr>

                  {/* Row 4: Typical Day-to-Day Work */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      <div className="flex items-center gap-1.5">
                        <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                        Typical Work Profile
                      </div>
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs text-slate-600 leading-relaxed">
                        {c.typical_work}
                      </td>
                    ))}
                  </tr>

                  {/* Row 5: Missing Skills & Readiness */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      <div className="flex items-center gap-1.5">
                        <Activity className="w-3.5 h-3.5 text-slate-400" />
                        Skill Prerequisites
                      </div>
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs">
                        <div className="font-semibold text-slate-800 mb-1">
                          {c.missing_skills_count > 0 ? (
                            <span className="text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                              {c.missing_skills_count} skill area(s) to bridge
                            </span>
                          ) : (
                            <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                              Strong existing foundation
                            </span>
                          )}
                        </div>
                        <div className="text-slate-500 mt-1">
                          Key: {c.key_skills_required.join(', ')}
                        </div>
                      </td>
                    ))}
                  </tr>

                  {/* Row 6: Learning Curve Complexity */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      Learning Curve
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs font-semibold text-slate-800">
                        {c.learning_curve_complexity}
                      </td>
                    ))}
                  </tr>

                  {/* Row 7: AI Future-Resilience */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      <div className="flex items-center gap-1.5">
                        <Cpu className="w-3.5 h-3.5 text-slate-400" />
                        AI Resilience Rating
                      </div>
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs font-semibold text-emerald-700">
                        {c.future_readiness_score}% Human-Centered Resilience
                      </td>
                    ))}
                  </tr>

                  {/* Row 8: Entry-Level Sample Role */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      Sample Entry Role
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs text-slate-700 font-medium">
                        {c.sample_entry_role}
                      </td>
                    ))}
                  </tr>

                  {/* Row 9: Tradeoff Synthesis */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      Tradeoff Summary
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5 text-xs text-slate-600 bg-brand-50/30">
                        {comparison.tradeoff_insights[c.career_name] || c.description}
                      </td>
                    ))}
                  </tr>

                  {/* Row 10: Direct Action CTAs */}
                  <tr>
                    <td className="p-4 sm:p-5 font-semibold text-slate-900 bg-slate-50/40 text-xs">
                      Take Action
                    </td>
                    {comparison.compared_careers.map((c) => (
                      <td key={c.career_id} className="p-4 sm:p-5">
                        <div className="space-y-2">
                          <Link
                            to={`/careers/${c.career_id}`}
                            className="w-full inline-flex items-center justify-center gap-1.5 bg-brand-600 hover:bg-brand-700 text-white font-medium py-2 px-3 rounded-xl text-xs transition-colors"
                          >
                            Explore Detail <ArrowUpRight className="w-3.5 h-3.5" />
                          </Link>
                          <Link
                            to={`/skill-gap/${c.career_id}`}
                            className="w-full inline-flex items-center justify-center gap-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-medium py-2 px-3 rounded-xl text-xs transition-colors"
                          >
                            Skill Gap Deep Dive
                          </Link>
                          <Link
                            to={`/roadmap?career=${c.career_id}`}
                            className="w-full inline-flex items-center justify-center gap-1.5 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 font-medium py-2 px-3 rounded-xl text-xs transition-colors"
                          >
                            Generate Roadmap
                          </Link>
                        </div>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center shadow-sm">
            <Compass className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <p className="text-base font-semibold text-slate-700">Select at least 2 careers to compare.</p>
          </div>
        )}
      </div>
    </div>
  );
};
