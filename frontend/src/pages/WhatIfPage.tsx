// frontend/src/pages/WhatIfPage.tsx
import React, { useState, useEffect } from 'react';
import {
  Sliders, Sparkles, TrendingUp, TrendingDown, Unlock, RotateCcw,
  Save, ArrowRight, ShieldCheck, CheckCircle2, AlertCircle, Compass
} from 'lucide-react';
import { api } from '../services/api';
import { WhatIfResponse, ScenarioDelta } from '../types';
import { CDIBadge } from '../components/CDIBadge';
import { CareerCard } from '../components/CareerCard';
import { Link } from 'react-router-dom';

export const WhatIfPage: React.FC = () => {
  // Input states
  const [programming, setProgramming] = useState<'none' | 'low' | 'moderate' | 'high'>('low');
  const [math, setMath] = useState<'low' | 'moderate' | 'high'>('moderate');
  const [creativity, setCreativity] = useState<'low' | 'moderate' | 'high'>('high');
  const [people, setPeople] = useState<'low' | 'balanced' | 'high'>('balanced');
  const [addedInterests, setAddedInterests] = useState<string[]>(['UI/UX Design']);
  const [newInterestInput, setNewInterestInput] = useState<string>('');

  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<WhatIfResponse | null>(null);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);

  const runSimulation = async (savePermanent: boolean = false) => {
    setLoading(true);
    setSaveSuccess(false);
    try {
      const data = await api.whatIf.simulate({
        programming_preference: programming,
        mathematics_preference: math,
        creativity_level: creativity,
        people_interaction_preference: people,
        added_interests: addedInterests,
        save_as_permanent: savePermanent,
      });
      setResult(data);
      if (savePermanent) {
        setSaveSuccess(true);
      }
    } catch (err) {
      console.error('Failed to run what-if simulation:', err);
    } finally {
      setLoading(false);
    }
  };

  // Run initial simulation on mount
  useEffect(() => {
    runSimulation();
  }, []);

  const handleAddInterest = (e: React.FormEvent) => {
    e.preventDefault();
    if (newInterestInput.trim() && !addedInterests.includes(newInterestInput.trim())) {
      setAddedInterests([...addedInterests, newInterestInput.trim()]);
      setNewInterestInput('');
    }
  };

  const removeInterest = (item: string) => {
    setAddedInterests(addedInterests.filter((i) => i !== item));
  };

  // Preset helper
  const applyPreset = (
    prog: 'none' | 'low' | 'moderate' | 'high',
    m: 'low' | 'moderate' | 'high',
    c: 'low' | 'moderate' | 'high',
    p: 'low' | 'balanced' | 'high',
    interests: string[]
  ) => {
    setProgramming(prog);
    setMath(m);
    setCreativity(c);
    setPeople(p);
    setAddedInterests(interests);
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
                  Novelty #4: Counterfactual Simulation
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 font-medium border border-emerald-200 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5" /> Zero Profile Risk
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
                <Sliders className="w-7 h-7 text-brand-600" />
                What-If Counterfactual Explorer
              </h1>
              <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-3xl">
                Test alternative hypotheses without modifying your base profile. See mathematically how tweaking programming, mathematics, or creative inclinations dynamically unlocks new career domains.
              </p>
            </div>

            {/* Presets dropdown / chips */}
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => applyPreset('low', 'moderate', 'high', 'balanced', ['UI/UX Design', 'Design Thinking'])}
                className="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold px-3 py-2 rounded-xl border border-indigo-200 transition-colors"
              >
                🎨 Creative Pivot
              </button>
              <button
                type="button"
                onClick={() => applyPreset('high', 'high', 'moderate', 'low', ['Machine Learning', 'Data Modeling'])}
                className="text-xs bg-cyan-50 hover:bg-cyan-100 text-cyan-800 font-semibold px-3 py-2 rounded-xl border border-cyan-200 transition-colors"
              >
                📊 High Quant / Tech
              </button>
              <button
                type="button"
                onClick={() => applyPreset('none', 'low', 'high', 'high', ['Product Strategy', 'Communication'])}
                className="text-xs bg-amber-50 hover:bg-amber-100 text-amber-800 font-semibold px-3 py-2 rounded-xl border border-amber-200 transition-colors"
              >
                🤝 People & Product
              </button>
            </div>
          </div>
        </div>

        {/* Two Column Workspace: Controls on Left, Simulated Deltas & Horizons on Right */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Controls Sandbox (4 cols) */}
          <div className="lg:col-span-4 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-6 h-fit sticky top-24">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Sliders className="w-4 h-4 text-brand-600" />
              Counterfactual Parameters
            </h2>

            {/* 1. Programming Slider */}
            <div>
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-2">
                <span>Programming Comfort</span>
                <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                  {programming}
                </span>
              </div>
              <div className="grid grid-cols-4 gap-1 bg-slate-100 p-1 rounded-xl">
                {(['none', 'low', 'moderate', 'high'] as const).map((opt) => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setProgramming(opt)}
                    className={`text-xs py-1.5 font-medium rounded-lg capitalize transition-all ${
                      programming === opt
                        ? 'bg-white text-brand-700 shadow-sm font-semibold'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            {/* 2. Mathematics Comfort */}
            <div>
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-2">
                <span>Mathematics / Quantitative</span>
                <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                  {math}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
                {(['low', 'moderate', 'high'] as const).map((opt) => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setMath(opt)}
                    className={`text-xs py-1.5 font-medium rounded-lg capitalize transition-all ${
                      math === opt
                        ? 'bg-white text-brand-700 shadow-sm font-semibold'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            {/* 3. Creativity Focus */}
            <div>
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-2">
                <span>Creativity & Visual Thinking</span>
                <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                  {creativity}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
                {(['low', 'moderate', 'high'] as const).map((opt) => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setCreativity(opt)}
                    className={`text-xs py-1.5 font-medium rounded-lg capitalize transition-all ${
                      creativity === opt
                        ? 'bg-white text-brand-700 shadow-sm font-semibold'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            {/* 4. People Interaction */}
            <div>
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-2">
                <span>Collaboration / People Work</span>
                <span className="capitalize text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded">
                  {people}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-xl">
                {(['low', 'balanced', 'high'] as const).map((opt) => (
                  <button
                    key={opt}
                    type="button"
                    onClick={() => setPeople(opt)}
                    className={`text-xs py-1.5 font-medium rounded-lg capitalize transition-all ${
                      people === opt
                        ? 'bg-white text-brand-700 shadow-sm font-semibold'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>

            {/* 5. Additional Virtual Interests */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-2">
                Simulated Extra Interests
              </label>
              <div className="flex flex-wrap gap-1.5 mb-2">
                {addedInterests.map((interest) => (
                  <span
                    key={interest}
                    className="inline-flex items-center gap-1 text-xs bg-brand-50 text-brand-700 border border-brand-200 px-2.5 py-1 rounded-lg font-medium"
                  >
                    {interest}
                    <button
                      type="button"
                      onClick={() => removeInterest(interest)}
                      className="hover:text-brand-900 font-bold ml-1"
                    >
                      &times;
                    </button>
                  </span>
                ))}
              </div>
              <form onSubmit={handleAddInterest} className="flex gap-2">
                <input
                  type="text"
                  placeholder="e.g. Design, Psychology..."
                  value={newInterestInput}
                  onChange={(e) => setNewInterestInput(e.target.value)}
                  className="flex-1 text-xs px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500"
                />
                <button
                  type="submit"
                  className="text-xs bg-slate-800 text-white font-medium px-3 py-2 rounded-xl hover:bg-slate-900"
                >
                  Add
                </button>
              </form>
            </div>

            {/* Trigger Button */}
            <div className="pt-2 space-y-2">
              <button
                type="button"
                onClick={() => runSimulation(false)}
                disabled={loading}
                className="w-full inline-flex items-center justify-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold py-3 px-4 rounded-xl text-sm transition-all shadow-md shadow-brand-500/20 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Simulating Perturbations...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    Simulate What-If Horizon
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={() => runSimulation(true)}
                disabled={loading}
                className="w-full inline-flex items-center justify-center gap-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-medium py-2.5 px-4 rounded-xl text-xs transition-colors"
              >
                <Save className="w-3.5 h-3.5 text-slate-500" />
                Commit to Permanent Profile
              </button>

              {saveSuccess && (
                <p className="text-xs text-emerald-600 font-medium text-center flex items-center justify-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Updated your permanent profile preferences!
                </p>
              )}
            </div>
          </div>

          {/* Results Showcase (8 cols) */}
          <div className="lg:col-span-8 space-y-6">
            {result ? (
              <>
                {/* Diversity Shift & Agent Rationale Banner */}
                <div className="bg-gradient-to-br from-brand-900 via-indigo-950 to-slate-900 rounded-2xl p-6 text-white shadow-lg space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-4">
                    <div>
                      <span className="text-xs font-semibold tracking-wider text-brand-300 uppercase">
                        Active Counterfactual Hypothesis
                      </span>
                      <h3 className="text-lg font-bold text-white mt-0.5">
                        {result.scenario_description}
                      </h3>
                    </div>

                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <div className="text-[11px] text-slate-300">Diversity Index (CDI)</div>
                        <div className="text-base font-extrabold text-emerald-400">
                          {result.diversity_index_what_if.toFixed(2)}
                        </div>
                      </div>
                      <span className="text-xs text-slate-400">vs</span>
                      <div className="text-left">
                        <div className="text-[11px] text-slate-300">Baseline CDI</div>
                        <div className="text-sm font-semibold text-slate-300">
                          {result.diversity_index_current.toFixed(2)}
                        </div>
                      </div>
                    </div>
                  </div>

                  <p className="text-sm text-brand-100 leading-relaxed">
                    {result.explanation}
                  </p>
                </div>

                {/* Significant Score Perturbations (Deltas) */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-base font-bold text-slate-900">
                        Counterfactual Score Deltas
                      </h3>
                      <p className="text-xs text-slate-500">
                        Careers whose compatibility shifted most noticeably under this simulated scenario.
                      </p>
                    </div>
                    <span className="text-xs font-medium text-slate-500">
                      {result.deltas.length} Significant shifts
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                    {result.deltas.map((delta) => {
                      const isSurged = delta.status === 'surged' || delta.status === 'newly_unlocked';
                      const isNewlyUnlocked = delta.status === 'newly_unlocked';

                      return (
                        <div
                          key={delta.career_id}
                          className={`p-4 rounded-xl border transition-all ${
                            isNewlyUnlocked
                              ? 'bg-purple-50/70 border-purple-200 ring-1 ring-purple-300'
                              : isSurged
                              ? 'bg-emerald-50/60 border-emerald-200'
                              : 'bg-rose-50/50 border-rose-200'
                          }`}
                        >
                          <div className="flex items-start justify-between gap-2 mb-1.5">
                            <div>
                              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-white/80 text-slate-700 uppercase tracking-wider border border-slate-200">
                                {delta.domain}
                              </span>
                              <h4 className="font-bold text-sm text-slate-900 mt-1">
                                {delta.career_name}
                              </h4>
                            </div>

                            <div className="text-right">
                              <span
                                className={`inline-flex items-center gap-0.5 text-xs font-bold px-2 py-0.5 rounded-md ${
                                  isNewlyUnlocked
                                    ? 'bg-purple-200 text-purple-900'
                                    : isSurged
                                    ? 'bg-emerald-200 text-emerald-900'
                                    : 'bg-rose-200 text-rose-900'
                                }`}
                              >
                                {isNewlyUnlocked ? (
                                  <>
                                    <Unlock className="w-3 h-3" /> UNLOCKED
                                  </>
                                ) : isSurged ? (
                                  <>
                                    <TrendingUp className="w-3 h-3" /> +{delta.score_change}%
                                  </>
                                ) : (
                                  <>
                                    <TrendingDown className="w-3 h-3" /> {delta.score_change}%
                                  </>
                                )}
                              </span>
                              <div className="text-[10px] text-slate-500 mt-0.5">
                                {delta.previous_score}% → {delta.new_score}%
                              </div>
                            </div>
                          </div>

                          <p className="text-xs text-slate-600 mt-2 line-clamp-2">
                            {delta.reason}
                          </p>

                          <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between">
                            <Link
                              to={`/careers/${delta.career_id}`}
                              className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1"
                            >
                              Explore Career <ArrowRight className="w-3 h-3" />
                            </Link>
                            <Link
                              to={`/skill-gap/${delta.career_id}`}
                              className="text-xs text-slate-500 hover:text-slate-800"
                            >
                              Check Skill Gap
                            </Link>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Side-by-Side Top Careers Comparison */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-4">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">
                      Top Viable Careers Under Counterfactual Simulation
                    </h3>
                    <p className="text-xs text-slate-500">
                      These careers represent your optimized frontier when the simulated conditions hold true.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                    {result.what_if_top_careers.map((c) => (
                      <CareerCard key={c.career_id} candidate={c} />
                    ))}
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-20 bg-white border border-slate-200 rounded-2xl">
                <Compass className="w-12 h-12 text-slate-300 mx-auto mb-3 animate-spin" />
                <p className="text-sm font-medium text-slate-600">Simulating counterfactual perturbations...</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
