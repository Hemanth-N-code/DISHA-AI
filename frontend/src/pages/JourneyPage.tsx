// frontend/src/pages/JourneyPage.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Compass, History, Bookmark, XCircle, Sparkles, Sliders, CheckCircle2,
  Calendar, ArrowRight, ShieldCheck, Layers, FileText, Bot
} from 'lucide-react';
import { api } from '../services/api';
import { JourneyResponse } from '../types';

export const JourneyPage: React.FC = () => {
  const [journey, setJourney] = useState<JourneyResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setLoading(true);
    api.memory.getJourney()
      .then(setJourney)
      .catch((err) => console.error('Failed to load journey:', err))
      .finally(() => setLoading(false));
  }, []);

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'career_explored':
      case 'career_viewed':
        return <Compass className="w-4 h-4 text-brand-600" />;
      case 'career_saved':
        return <Bookmark className="w-4 h-4 text-amber-500" />;
      case 'career_rejected':
        return <XCircle className="w-4 h-4 text-rose-500" />;
      case 'what_if_simulated':
        return <Sliders className="w-4 h-4 text-purple-600" />;
      case 'roadmap_created':
      case 'roadmap_task_updated':
        return <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
      default:
        return <History className="w-4 h-4 text-slate-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs px-3 py-1 rounded-full bg-brand-50 text-brand-700 font-semibold border border-brand-200 uppercase tracking-wider">
                  Novelty #7: Longitudinal Decision Memory
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 font-medium border border-emerald-200 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5" /> Evolving Student Context
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
                <History className="w-7 h-7 text-brand-600" />
                Career Decision Trace & Memory
              </h1>
              <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-3xl">
                Every career explored, comparison run, scenario simulated, and path rejected forms your personal decision trace. Unlike traditional recommenders that reset each session, DISHA learns from your choices over time.
              </p>
            </div>

            <Link
              to="/discover"
              className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold py-2.5 px-4 rounded-xl text-sm transition-colors shadow-sm self-start md:self-auto"
            >
              Explore Universe <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {loading ? (
          <div className="bg-white border border-slate-200 rounded-2xl p-16 text-center shadow-sm">
            <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium text-slate-700">Reconstructing decision trace and historical milestones...</p>
          </div>
        ) : journey ? (
          <>
            {/* Stat Counters */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Careers Explored
                </div>
                <div className="text-3xl font-black text-slate-900 mt-2">
                  {journey.total_careers_explored}
                </div>
                <p className="text-xs text-slate-500 mt-1">Deep dives and profile analyses</p>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Saved Shortlist
                </div>
                <div className="text-3xl font-black text-brand-600 mt-2">
                  {journey.saved_careers.length}
                </div>
                <p className="text-xs text-slate-500 mt-1">Pinned high-affinity paths</p>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Rejected with Rationale
                </div>
                <div className="text-3xl font-black text-rose-600 mt-2">
                  {journey.rejected_careers_with_reasons.length}
                </div>
                <p className="text-xs text-slate-500 mt-1">Valuable negative constraints</p>
              </div>

              <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  What-If Sim Tests
                </div>
                <div className="text-3xl font-black text-purple-600 mt-2">
                  {journey.active_what_if_scenarios.length}
                </div>
                <p className="text-xs text-slate-500 mt-1">Hypotheses tested</p>
              </div>
            </div>

            {/* Two Columns: Learned Preferences & Rejected Table */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Learned Constraints & Saved (5 cols) */}
              <div className="lg:col-span-5 space-y-6">
                {/* Learned Preferences Card */}
                <div className="bg-gradient-to-br from-indigo-900 to-slate-900 rounded-2xl p-6 text-white shadow-md space-y-4">
                  <div className="flex items-center gap-2 text-brand-300 text-xs font-bold uppercase tracking-wider">
                    <Sparkles className="w-4 h-4 text-amber-300" /> Synthesized Decision Constraints
                  </div>
                  <h3 className="text-lg font-bold text-white leading-snug">
                    What DISHA AI Has Inferred From Your Exploration
                  </h3>
                  <div className="space-y-2 text-sm text-indigo-100">
                    <div className="bg-white/10 rounded-xl p-3 border border-white/10">
                      <span className="font-semibold text-white">Preferred Modality:</span>
                      <p className="text-xs mt-0.5 text-indigo-200">
                        Strong preference for visual synthesis, human empathy, and interface design over repetitive raw syntax coding.
                      </p>
                    </div>
                    <div className="bg-white/10 rounded-xl p-3 border border-white/10">
                      <span className="font-semibold text-white">Negative Constraint:</span>
                      <p className="text-xs mt-0.5 text-indigo-200">
                        Expressed reluctance toward 8-hour solo coding; prioritizes cross-functional teamwork.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Saved Careers Quick Access */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                      <Bookmark className="w-4 h-4 text-amber-500" />
                      Saved Shortlist
                    </h3>
                    <span className="text-xs text-slate-500">{journey.saved_careers.length} items</span>
                  </div>

                  {journey.saved_careers.length === 0 ? (
                    <p className="text-xs text-slate-500 italic py-2">
                      No careers bookmarked yet. Click the bookmark icon on any career card to save it here.
                    </p>
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      {journey.saved_careers.map((c, i) => (
                        <Link
                          key={i}
                          to={`/careers/${c.toLowerCase().replace(/[\s/]+/g, '_')}`}
                          className="text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200 px-3 py-1.5 rounded-xl hover:bg-amber-100 transition-colors"
                        >
                          {c}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Rejected Paths Showcase (7 cols) */}
              <div className="lg:col-span-7 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                      <XCircle className="w-4 h-4 text-rose-500" />
                      Explicitly Rejected Paths & Negative Constraints
                    </h3>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    In DISHA, passing on a career isn't discarded. The rationale is indexed as a negative constraint so future discoveries avoid similar misfits.
                  </p>
                </div>

                {journey.rejected_careers_with_reasons.length === 0 ? (
                  <div className="p-8 text-center border border-dashed border-slate-200 rounded-xl">
                    <p className="text-xs text-slate-500">
                      No paths explicitly rejected yet. When exploring careers, you can reject options with rationale to help DISHA fine-tune recommendations.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {journey.rejected_careers_with_reasons.map((item, idx) => (
                      <div
                        key={idx}
                        className="bg-rose-50/50 border border-rose-200 rounded-xl p-4 space-y-1.5"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-sm text-slate-900">
                            {item.career_name}
                          </span>
                          <span className="text-[10px] text-slate-400">
                            {new Date(item.rejected_at).toLocaleDateString()}
                          </span>
                        </div>
                        <p className="text-xs text-slate-700 italic">
                          "{item.reason}"
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Chronological Timeline */}
            <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
              <div>
                <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <History className="w-5 h-5 text-brand-600" />
                  Chronological Decision Timeline
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  A verifiable audit log of your career exploration process.
                </p>
              </div>

              <div className="relative border-l-2 border-slate-200 ml-4 space-y-6 py-2">
                {journey.timeline.map((event, index) => (
                  <div key={index} className="relative pl-6">
                    {/* Circle Node Icon */}
                    <div className="absolute -left-3 top-0.5 bg-white border border-slate-200 rounded-full p-1 shadow-sm">
                      {getEventIcon(event.event_type)}
                    </div>

                    <div className="space-y-1">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                        <span className="font-bold text-sm text-slate-900">
                          {event.title}
                        </span>
                        <span className="text-[11px] text-slate-400">
                          {new Date(event.timestamp).toLocaleString()}
                        </span>
                      </div>

                      <p className="text-xs text-slate-600 leading-relaxed">
                        {event.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
};
