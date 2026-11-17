// frontend/src/pages/LandingPage.tsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Compass, Sparkles, Scale, Network, ListTodo,
  ArrowRight, ShieldCheck, CheckCircle2, TrendingUp,
  Cpu, Layers, BookOpen, UserCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LandingPage: React.FC = () => {
  const { user, quickDemoLogin } = useAuth();
  const navigate = useNavigate();

  const handleDemoLaunch = async () => {
    await quickDemoLogin();
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28 border-b border-slate-200 bg-gradient-to-b from-white via-indigo-50/30 to-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          {/* Research Pill */}
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-50 border border-brand-200 text-brand-800 text-xs font-semibold mb-6 shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-brand-600" />
            <span>Research Novelty: Career Decision Exploration vs. One-Shot Recommendation</span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight max-w-4xl mx-auto leading-tight sm:leading-tight">
            Discover Your Direction.{' '}
            <span className="bg-gradient-to-r from-brand-600 via-indigo-600 to-cyan-600 bg-clip-text text-transparent">
              Shape Your Future.
            </span>
          </h1>

          {/* Subtext */}
          <p className="mt-6 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Explore diverse career universes beyond popular algorithms, simulate counterfactual "What-If" scenarios,
            diagnose real skill gaps, and translate your ambitions into an actionable roadmap.
          </p>

          {/* CTA Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            {user ? (
              <Link
                to="/dashboard"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm shadow-md shadow-brand-500/25 transition-all"
              >
                <span>Go to My Dashboard</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            ) : (
              <>
                <Link
                  to="/signup"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm shadow-md shadow-brand-500/25 transition-all"
                >
                  <span>Find My Direction</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <button
                  onClick={handleDemoLaunch}
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold text-sm shadow-sm transition-all"
                >
                  <Sparkles className="w-4 h-4 text-amber-600" />
                  <span>Launch 1-Click Demo Scenario</span>
                </button>
              </>
            )}
            <Link
              to="/discover"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 font-semibold text-sm transition-all"
            >
              <span>Explore 110+ Careers Universe</span>
            </Link>
          </div>

          {/* Research Metric Teaser */}
          <div className="mt-12 inline-flex items-center gap-6 text-xs text-slate-500 bg-white/80 backdrop-blur px-5 py-2.5 rounded-2xl border border-slate-200 shadow-sm">
            <div>
              <span className="font-bold text-slate-900 text-sm">17</span> Domains Maintained
            </div>
            <div className="h-4 w-px bg-slate-200" />
            <div>
              <span className="font-bold text-slate-900 text-sm">0.885</span> Career Diversity Index
            </div>
            <div className="h-4 w-px bg-slate-200" />
            <div>
              <span className="font-bold text-emerald-600 text-sm">+53%</span> Decision Clarity
            </div>
          </div>
        </div>
      </section>

      {/* Visual Workflow Section: DISCOVER -> EXPLORE -> COMPARE -> UNDERSTAND -> PLAN */}
      <section className="py-16 bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-xs uppercase font-extrabold tracking-wider text-brand-600 mb-2">The DISHA Framework</h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-900">
              Not Just a Career Recommendation. A Complete Decision Framework.
            </h3>
            <p className="mt-3 text-sm text-slate-600">
              Traditional platforms assign you a fixed job title. DISHA guides your cognition through systematic decision milestones.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {/* Step 1 */}
            <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-white hover:shadow-md transition-all">
              <div className="w-8 h-8 rounded-lg bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-sm mb-3">
                1
              </div>
              <h4 className="font-bold text-slate-900 text-sm mb-1">DISCOVER</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Break out of popularity bias with diversity-aware discovery spanning 17 domains.
              </p>
            </div>

            {/* Step 2 */}
            <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-white hover:shadow-md transition-all">
              <div className="w-8 h-8 rounded-lg bg-cyan-100 text-cyan-800 flex items-center justify-center font-bold text-sm mb-3">
                2
              </div>
              <h4 className="font-bold text-slate-900 text-sm mb-1">EXPLORE</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Traverse the Alternative Path Graph to see how careers pivot into adjacent roles.
              </p>
            </div>

            {/* Step 3 */}
            <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-white hover:shadow-md transition-all">
              <div className="w-8 h-8 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center font-bold text-sm mb-3">
                3
              </div>
              <h4 className="font-bold text-slate-900 text-sm mb-1">COMPARE</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Neutral, multi-dimensional trade-off analysis across 2-4 pathways without an arbitrary winner.
              </p>
            </div>

            {/* Step 4 */}
            <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-white hover:shadow-md transition-all">
              <div className="w-8 h-8 rounded-lg bg-purple-100 text-purple-800 flex items-center justify-center font-bold text-sm mb-3">
                4
              </div>
              <h4 className="font-bold text-slate-900 text-sm mb-1">UNDERSTAND</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Simulate "What-If" constraint shifts and inspect task-level automation/augmentation risks.
              </p>
            </div>

            {/* Step 5 */}
            <div className="p-5 rounded-xl border border-slate-200 bg-slate-50/60 hover:bg-white hover:shadow-md transition-all">
              <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold text-sm mb-3">
                5
              </div>
              <h4 className="font-bold text-slate-900 text-sm mb-1">PLAN</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Convert your diagnosed skill gap into an editable, portfolio-centric milestone DAG.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Novelty Comparison Matrix */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-10">
            <h3 className="text-2xl font-bold text-slate-900">Why DISHA Stands Apart</h3>
            <p className="text-sm text-slate-600 mt-2">
              Comparing standard IEEE career recommender baselines with the DISHA Framework.
            </p>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200">
              {/* Conventional */}
              <div className="p-6 sm:p-8 bg-slate-50/50">
                <div className="flex items-center gap-2 mb-4 text-slate-500 font-bold text-sm uppercase tracking-wider">
                  <span>Conventional Recommender Systems</span>
                </div>
                <ul className="space-y-3.5 text-xs text-slate-600">
                  <li className="flex items-start gap-2.5">
                    <span className="text-red-500 font-bold">&times;</span>
                    <span><strong>One-shot static prediction:</strong> Computes top-5 job matches and terminates interaction.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <span className="text-red-500 font-bold">&times;</span>
                    <span><strong>Popularity bias:</strong> Over-recommends software developer roles to all STEM students.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <span className="text-red-500 font-bold">&times;</span>
                    <span><strong>Passive student role:</strong> No ability to test counterfactuals like "What if I avoid heavy coding?"</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <span className="text-red-500 font-bold">&times;</span>
                    <span><strong>Disconnected action:</strong> Generates generic course links without milestone tracking.</span>
                  </li>
                </ul>
              </div>

              {/* DISHA */}
              <div className="p-6 sm:p-8 bg-brand-50/30">
                <div className="flex items-center gap-2 mb-4 text-brand-700 font-bold text-sm uppercase tracking-wider">
                  <Sparkles className="w-4 h-4 text-brand-600" />
                  <span>The DISHA AI Framework</span>
                </div>
                <ul className="space-y-3.5 text-xs text-slate-700">
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong>Iterative decision exploration:</strong> Careers are graph nodes, not static endpoints.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong>Diversity-aware discovery (CDI):</strong> Actively surfaces non-obvious high-affinity careers.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong>Counterfactual "What-If" agency:</strong> Perturb preferences and observe Pareto recalculations live.</span>
                  </li>
                  <li className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong>Longitudinal decision memory:</strong> Remembers explored/rejected paths and preserves roadmap progress.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Target Audience / Call to Action */}
      <section className="py-14 bg-gradient-to-tr from-brand-900 to-indigo-900 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h3 className="text-2xl sm:text-3xl font-black mb-4">
            Are You Completing 12th / Intermediate / PUC?
          </h3>
          <p className="text-indigo-200 text-sm sm:text-base mb-8 max-w-xl mx-auto leading-relaxed">
            Take control of your decision. Explore alternatives before committing years to a single degree.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/signup"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-white text-brand-900 font-bold text-sm shadow-lg hover:bg-indigo-50 transition-all"
            >
              Start Free Student Onboarding
            </Link>
            <button
              onClick={handleDemoLaunch}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-amber-400 text-amber-950 font-bold text-sm shadow-lg hover:bg-amber-300 transition-all"
            >
              Try Instant Demo Account
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};
