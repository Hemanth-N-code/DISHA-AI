// frontend/src/pages/SkillGapPage.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend
} from 'recharts';
import {
  Target, CheckCircle2, AlertTriangle, ArrowRight, BookOpen,
  Sparkles, Clock, Calendar, ArrowLeft, Layers, Compass
} from 'lucide-react';
import { api } from '../services/api';
import { SkillGapResponse, CareerDetail } from '../types';

export const SkillGapPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const currentCareerId = id || 'ux_designer';

  const [gapData, setGapData] = useState<SkillGapResponse | null>(null);
  const [careerList, setCareerList] = useState<CareerDetail[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [viewMode, setViewMode] = useState<'radar' | 'bar'>('radar');

  useEffect(() => {
    api.careers.list().then((list) => setCareerList(list)).catch(console.warn);
  }, []);

  useEffect(() => {
    setLoading(true);
    api.skillGap.get(currentCareerId)
      .then((data) => {
        setGapData(data);
      })
      .catch((err) => {
        console.error('Failed to load skill gap data:', err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [currentCareerId]);

  // Format data for Recharts
  const chartData = gapData?.skills_breakdown.map((s) => ({
    skill: s.skill_name,
    current: s.current_level,
    required: s.required_level,
    gap: s.gap,
  })) || [];

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header & Career Selector */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Link
                  to={`/careers/${currentCareerId}`}
                  className="p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  <ArrowLeft className="w-4 h-4" />
                </Link>
                <span className="text-xs px-3 py-1 rounded-full bg-brand-50 text-brand-700 font-semibold border border-brand-200 uppercase tracking-wider">
                  Novelty #6: Deterministic Skill Gap Analysis
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
                <Target className="w-7 h-7 text-brand-600" />
                Prerequisite & Skill Gap Analyzer
              </h1>
              <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-3xl">
                Evaluates your current proficiencies (1-5) against the empirical industry demands of this role. Every identified gap comes with an actionable bridge so you know exactly what to learn.
              </p>
            </div>

            {/* Target Career Switcher */}
            <div className="flex items-center gap-2">
              <label className="text-xs font-medium text-slate-600">Career Focus:</label>
              <select
                value={currentCareerId}
                onChange={(e) => navigate(`/skill-gap/${e.target.value}`)}
                className="text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
              >
                {careerList.map((c) => (
                  <option key={c.career_id} value={c.career_id}>
                    {c.career_name} ({c.domain})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="bg-white border border-slate-200 rounded-2xl p-16 text-center shadow-sm">
            <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium text-slate-700">Evaluating skill vectors and prerequisite proficiencies...</p>
          </div>
        ) : gapData ? (
          <>
            {/* Top Stat Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Overall Readiness
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-brand-600">
                    {gapData.readiness_percentage}%
                  </span>
                  <span className="text-xs text-slate-500">of required skills</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full mt-3 overflow-hidden">
                  <div
                    className="bg-brand-600 h-full rounded-full"
                    style={{ width: `${gapData.readiness_percentage}%` }}
                  />
                </div>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Foundation Match
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-emerald-600">
                    {gapData.matched_skills_count}
                  </span>
                  <span className="text-xs text-slate-500">of {gapData.total_skills_evaluated} skills satisfied</span>
                </div>
                <p className="text-xs text-emerald-600 font-medium mt-2 flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Proficient or meeting benchmark
                </p>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Critical Gaps to Bridge
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-amber-600">
                    {gapData.gap_skills_count}
                  </span>
                  <span className="text-xs text-slate-500">skills require upskilling</span>
                </div>
                <p className="text-xs text-amber-600 font-medium mt-2 flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5" /> High-impact bridge areas
                </p>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Estimated Timeline
                </div>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-indigo-600">
                    {gapData.estimated_upskilling_months}
                  </span>
                  <span className="text-xs text-slate-500">Months of focused effort</span>
                </div>
                <p className="text-xs text-indigo-600 font-medium mt-2 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" /> ~10 hours per week
                </p>
              </div>
            </div>

            {/* Visualizer Chart & Action Banner */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Radar/Bar Chart (7 cols) */}
              <div className="lg:col-span-7 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">
                      Proficiency Profile vs Industry Benchmark
                    </h3>
                    <p className="text-xs text-slate-500">
                      Comparing student level (0-5) against expected industry level (1-5).
                    </p>
                  </div>

                  <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl text-xs font-medium">
                    <button
                      onClick={() => setViewMode('radar')}
                      className={`px-3 py-1 rounded-lg transition-all ${
                        viewMode === 'radar'
                          ? 'bg-white text-slate-900 shadow-sm font-semibold'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      Radar View
                    </button>
                    <button
                      onClick={() => setViewMode('bar')}
                      className={`px-3 py-1 rounded-lg transition-all ${
                        viewMode === 'bar'
                          ? 'bg-white text-slate-900 shadow-sm font-semibold'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      Bar View
                    </button>
                  </div>
                </div>

                <div className="h-[340px] w-full flex items-center justify-center">
                  <ResponsiveContainer width="100%" height="100%">
                    {viewMode === 'radar' ? (
                      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                        <PolarGrid stroke="#e2e8f0" />
                        <PolarAngleAxis dataKey="skill" tick={{ fill: '#475569', fontSize: 11 }} />
                        <PolarRadiusAxis angle={30} domain={[0, 5]} stroke="#cbd5e1" />
                        <Radar
                          name="Your Current Level"
                          dataKey="current"
                          stroke="#6366f1"
                          fill="#6366f1"
                          fillOpacity={0.4}
                        />
                        <Radar
                          name="Required Benchmark"
                          dataKey="required"
                          stroke="#0891b2"
                          fill="#0891b2"
                          fillOpacity={0.2}
                        />
                        <Legend />
                        <Tooltip />
                      </RadarChart>
                    ) : (
                      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                        <XAxis dataKey="skill" tick={{ fill: '#475569', fontSize: 11 }} interval={0} angle={-20} textAnchor="end" />
                        <YAxis domain={[0, 5]} tick={{ fill: '#475569', fontSize: 11 }} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="current" name="Your Current Level" fill="#6366f1" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="required" name="Required Benchmark" fill="#cbd5e1" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    )}
                  </ResponsiveContainer>
                </div>

                <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-brand-500" /> Current Proficiency
                  </span>
                  <span className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-cyan-600" /> Target Industry Level
                  </span>
                </div>
              </div>

              {/* Action & Transition Card (5 cols) */}
              <div className="lg:col-span-5 bg-gradient-to-br from-indigo-900 to-slate-900 rounded-2xl p-6 text-white flex flex-col justify-between shadow-lg">
                <div className="space-y-4">
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 text-brand-200 text-xs font-semibold backdrop-blur-sm">
                    <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                    Actionable Roadmap Conversion
                  </div>

                  <h3 className="text-xl font-bold text-white leading-snug">
                    Turn These {gapData.gap_skills_count} Skill Gaps into a Structured {gapData.estimated_upskilling_months}-Month Roadmap
                  </h3>

                  <p className="text-sm text-indigo-100 leading-relaxed">
                    DISHA converts every missing proficiency into milestone-driven projects, curriculum modules, and verifiable portfolio deliverables.
                  </p>

                  <div className="bg-white/10 rounded-xl p-4 space-y-2 border border-white/10">
                    <div className="text-xs font-semibold text-brand-200 uppercase tracking-wider">
                      Priority Focus Areas
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {gapData.top_priority_focus_areas.map((area, i) => (
                        <span
                          key={i}
                          className="text-xs bg-brand-500/30 text-white border border-brand-400/40 px-2.5 py-1 rounded-lg font-medium"
                        >
                          {area}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="pt-6">
                  <Link
                    to={`/roadmap?career=${currentCareerId}`}
                    className="w-full inline-flex items-center justify-center gap-2 bg-brand-500 hover:bg-brand-400 text-white font-bold py-3.5 px-5 rounded-xl text-sm transition-all shadow-md shadow-brand-500/30"
                  >
                    Generate Milestone Roadmap
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </div>

            {/* Granular Breakdown List */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
              <div>
                <h3 className="text-lg font-bold text-slate-900">
                  Granular Skill-by-Skill Action Plan
                </h3>
                <p className="text-xs text-slate-500">
                  Concrete, prioritized recommendations for each skill prerequisite.
                </p>
              </div>

              <div className="divide-y divide-slate-100">
                {gapData.skills_breakdown.map((item, idx) => {
                  const isCritical = item.priority === 'Critical';
                  const isHigh = item.priority === 'High';
                  const isMatched = item.category === 'existing';

                  return (
                    <div key={idx} className="py-4 first:pt-0 last:pb-0 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="space-y-1 sm:max-w-md">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-sm text-slate-900">
                            {item.skill_name}
                          </span>
                          <span
                            className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                              isMatched
                                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                : isCritical
                                ? 'bg-rose-50 text-rose-700 border border-rose-200'
                                : 'bg-amber-50 text-amber-700 border border-amber-200'
                            }`}
                          >
                            {isMatched ? 'Satisfied' : `${item.priority} Priority`}
                          </span>
                        </div>
                        <p className="text-xs text-slate-600">
                          {item.recommended_action}
                        </p>
                      </div>

                      <div className="flex items-center gap-6 sm:justify-end">
                        <div className="text-right">
                          <div className="text-[10px] text-slate-400 uppercase font-semibold">Your Level</div>
                          <div className="text-sm font-bold text-brand-600">
                            Level {item.current_level} / 5
                          </div>
                        </div>

                        <div className="text-right">
                          <div className="text-[10px] text-slate-400 uppercase font-semibold">Required</div>
                          <div className="text-sm font-bold text-slate-800">
                            Level {item.required_level} / 5
                          </div>
                        </div>

                        <div className="text-right min-w-[70px]">
                          <div className="text-[10px] text-slate-400 uppercase font-semibold">Gap</div>
                          <div className={`text-sm font-bold ${item.gap > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
                            {item.gap > 0 ? `-${item.gap}` : '0 (Met)'}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
};
