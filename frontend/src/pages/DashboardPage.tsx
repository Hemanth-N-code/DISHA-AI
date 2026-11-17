// frontend/src/pages/DashboardPage.tsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Sparkles, Compass, Bookmark, ListTodo, History,
  ArrowRight, CheckCircle2, TrendingUp, BookOpen, AlertCircle, Scale, GraduationCap
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { StudentProfile, CareerCandidate, Roadmap, JourneyResponse } from '../types';
import { CareerCard } from '../components/CareerCard';
import { CDIBadge } from '../components/CDIBadge';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [candidates, setCandidates] = useState<CareerCandidate[]>([]);
  const [cdi, setCdi] = useState<number>(0.85);
  const [roadmaps, setRoadmaps] = useState<Roadmap[]>([]);
  const [journey, setJourney] = useState<JourneyResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      setLoading(true);
      try {
        const p = await api.profile.get();
        setProfile(p);

        // Fetch top diversity-aware discoveries
        const disc = await api.careers.discover(true);
        setCandidates(disc.candidates.slice(0, 4));
        setCdi(disc.career_diversity_index);

        // Fetch roadmaps & journey
        const rms = await api.roadmap.getActive('ux_designer').catch(() => null);
        if (rms) setRoadmaps([rms]);
        
        const j = await api.memory.getJourney().catch(() => null);
        if (j) setJourney(j);
      } catch (err) {
        console.warn('Dashboard load error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-3">
        <div className="w-8 h-8 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin" />
        <p className="text-xs text-slate-500 font-medium">Synthesizing your decision dashboard...</p>
      </div>
    );
  }

  // If no profile completed yet, prompt onboarding
  if (!profile) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white rounded-2xl border border-slate-200 text-center shadow-sm">
        <div className="w-12 h-12 rounded-full bg-brand-50 text-brand-600 flex items-center justify-center mx-auto mb-4">
          <Compass className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900 mb-2">Complete Student Onboarding</h2>
        <p className="text-xs text-slate-600 mb-6">
          To generate transparent career compatibility scores, diversity-aware paths, and skill gap graphs, please complete your onboarding.
        </p>
        <Link
          to="/onboarding"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-brand-600 text-white font-semibold text-xs shadow-sm hover:bg-brand-700"
        >
          <span>Start Onboarding Calibration</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-brand-900 via-indigo-900 to-slate-900 rounded-2xl p-6 sm:p-8 text-white shadow-md relative overflow-hidden">
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-brand-800/80 border border-brand-700 text-brand-200 text-[11px] font-semibold mb-3">
            <Sparkles className="w-3 h-3 text-amber-400" />
            <span>Profile Archetype: {profile.academic_strengths?.[0] || 'Calibrated Student Explorer'}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black tracking-tight">
            Welcome back, {user?.full_name?.split(' ')[0] || 'Explorer'}!
          </h1>
          <p className="text-indigo-200 text-xs sm:text-sm mt-2 leading-relaxed">
            {profile.profile_summary || 'Your profile is calibrated for multi-domain career exploration.'}
          </p>

          {/* Quick Action Pills */}
          <div className="mt-5 flex flex-wrap gap-2.5 text-xs">
            <Link
              to="/what-if"
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 font-medium transition-colors"
            >
              <Compass className="w-3.5 h-3.5 text-amber-300" />
              <span>Simulate: "What if less coding?"</span>
            </Link>
            <Link
              to="/graph?center=ux_designer"
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 font-medium transition-colors"
            >
              <TrendingUp className="w-3.5 h-3.5 text-cyan-300" />
              <span>Inspect UX Design Path Graph</span>
            </Link>
            <Link
              to="/compare"
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 font-medium transition-colors"
            >
              <Scale className="w-3.5 h-3.5 text-pink-300" />
              <span>Compare UX vs Data Analyst</span>
            </Link>
          </div>
        </div>
      </div>

      {/* CET-Support Entrance Exam Callout */}
      <div className="bg-gradient-to-r from-emerald-950 via-slate-900 to-teal-950 rounded-2xl p-5 sm:p-6 text-white border border-emerald-800/40 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold uppercase tracking-wider">
            <GraduationCap className="w-3.5 h-3.5" />
            <span>New Feature: KCET & State Entrance Support</span>
          </div>
          <h2 className="text-lg font-bold">Have a KCET or State Entrance Exam Rank?</h2>
          <p className="text-xs text-slate-300 leading-relaxed">
            Bridge your rank with 2023–2025 closing cutoffs, verified NIRF placement reports, and build a safe, structured Option Entry preference list for KEA counselling.
          </p>
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          <Link
            to="/cet"
            className="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs rounded-xl shadow-sm transition-colors whitespace-nowrap flex items-center gap-1.5"
          >
            <span>Explore KCET Colleges</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
          <Link
            to="/cet/option-list"
            className="px-3.5 py-2.5 bg-white/10 hover:bg-white/20 text-white font-semibold text-xs rounded-xl transition-colors whitespace-nowrap"
          >
            <span>My Option List</span>
          </Link>
        </div>
      </div>

      {/* Metrics & Status Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: CDI Diversity Badge */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
            <span className="font-semibold uppercase tracking-wider">Career Diversity</span>
            <Sparkles className="w-4 h-4 text-brand-600" />
          </div>
          <div className="text-2xl font-black text-brand-700">{cdi.toFixed(3)}</div>
          <p className="text-[11px] text-slate-500 mt-1">Multi-domain span index (non-popularity biased)</p>
        </div>

        {/* Card 2: Explored Careers */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
            <span className="font-semibold uppercase tracking-wider">Explored Paths</span>
            <History className="w-4 h-4 text-cyan-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">
            {journey?.total_careers_explored || 0}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Recorded in persistent decision memory</p>
        </div>

        {/* Card 3: Saved Shortlist */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
            <span className="font-semibold uppercase tracking-wider">Shortlisted</span>
            <Bookmark className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-black text-slate-900">
            {journey?.saved_careers?.length || 0}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Active candidates under evaluation</p>
        </div>

        {/* Card 4: Active Roadmap Progress */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center justify-between text-xs text-slate-500 mb-2">
            <span className="font-semibold uppercase tracking-wider">Active Roadmap</span>
            <ListTodo className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-black text-emerald-600">
            {roadmaps[0]?.overall_progress ? `${roadmaps[0].overall_progress}%` : 'Ready'}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">
            {roadmaps[0]?.career_name ? `Target: ${roadmaps[0].career_name}` : 'Generate your first roadmap'}
          </p>
        </div>
      </div>

      {/* Suggested Explorations & CDI Discovery */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-slate-900 tracking-tight">
              Curated Career Universe Discovery
            </h2>
            <p className="text-xs text-slate-500">
              Surfacing high-compatibility options with diversity optimization across multiple domains.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <CDIBadge score={cdi} domainsCount={4} strategy="Diversity-Aware" />
            <Link
              to="/discover"
              className="text-xs font-bold text-brand-600 hover:text-brand-700 inline-flex items-center gap-1"
            >
              <span>View All 110+</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {candidates.map((cand) => (
            <CareerCard key={cand.career_id} candidate={cand} />
          ))}
        </div>
      </div>

      {/* Quick What-If Experimentation Callout */}
      <div className="bg-gradient-to-r from-amber-500/10 via-orange-500/10 to-brand-500/10 rounded-2xl p-6 border border-amber-200/80 flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-bold text-amber-900 uppercase tracking-wider">
            <Compass className="w-4 h-4 text-amber-600" />
            <span>Counterfactual Decision Experiment</span>
          </div>
          <h3 className="text-base font-bold text-slate-900">
            Wondering what happens if your preferences change?
          </h3>
          <p className="text-xs text-slate-600 max-w-2xl leading-relaxed">
            Unlike static recommenders that force you into a box, DISHA's counterfactual engine recalculates career fits in real-time.
            Test scenarios like <em>"What if I prefer creative work over coding?"</em> without overwriting your profile.
          </p>
        </div>
        <Link
          to="/what-if"
          className="shrink-0 inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs shadow-sm transition-colors"
        >
          <span>Open What-If Lab</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
};
