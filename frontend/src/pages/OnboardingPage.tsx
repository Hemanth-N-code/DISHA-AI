// frontend/src/pages/OnboardingPage.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Check, ArrowRight, ArrowLeft, Brain, Sliders, Target, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

export const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form State
  const [stream, setStream] = useState('Science (PCM)');
  const [marksPercentage, setMarksPercentage] = useState<number>(82);
  const [favoriteSubjects, setFavoriteSubjects] = useState<string[]>(['Mathematics', 'Computer Science']);
  
  const [interests, setInterests] = useState<string[]>(['Technology', 'Design']);
  const [skills, setSkills] = useState<{ skill: string; level: number }[]>([
    { skill: 'Basic Programming', level: 2 },
    { skill: 'Creativity', level: 4 },
    { skill: 'Communication', level: 4 },
    { skill: 'Problem Solving', level: 3 }
  ]);

  const [programmingPref, setProgrammingPref] = useState<'none' | 'low' | 'moderate' | 'high'>('low');
  const [mathPref, setMathPref] = useState<'low' | 'moderate' | 'high'>('moderate');
  const [creativityPref, setCreativityPref] = useState<'low' | 'moderate' | 'high'>('high');
  const [peoplePref, setPeoplePref] = useState<'low' | 'balanced' | 'high'>('balanced');

  const [goals, setGoals] = useState<string[]>(['Higher studies', 'Creative career in technology']);
  const [constraints, setConstraints] = useState<string[]>(['Prefers less heavy coding', 'Willing to relocate']);

  const streamOptions = [
    'Science (PCM)',
    'Science (PCB)',
    'Commerce',
    'Arts/Humanities',
    'Vocational / General'
  ];

  const interestOptions = [
    'Technology', 'AI / Data', 'Design', 'Business & Finance', 'Arts & Media',
    'Psychology', 'Healthcare', 'Law', 'Environment', 'Research', 'Social Impact'
  ];

  const toggleInterest = (item: string) => {
    if (interests.includes(item)) {
      setInterests(interests.filter((i) => i !== item));
    } else {
      setInterests([...interests, item]);
    }
  };

  const handlePrefillDemo = () => {
    setStream('Science (PCM)');
    setMarksPercentage(84);
    setFavoriteSubjects(['Mathematics', 'Computer Science']);
    setInterests(['Technology', 'Design']);
    setSkills([
      { skill: 'Basic Programming', level: 2 },
      { skill: 'Creativity', level: 4 },
      { skill: 'Communication', level: 4 },
      { skill: 'Problem Solving', level: 3 }
    ]);
    setProgrammingPref('low');
    setMathPref('moderate');
    setCreativityPref('high');
    setPeoplePref('balanced');
    setGoals(['Higher studies', 'Creative career in technology']);
    setConstraints(['Prefers less heavy coding', 'Willing to relocate']);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      await api.profile.createOrUpdate({
        education_level: '12th / Intermediate / PUC',
        stream,
        subjects: favoriteSubjects,
        marks_percentage: Number(marksPercentage),
        favorite_subjects: favoriteSubjects,
        interests,
        skills,
        preferences: [
          `Programming: ${programmingPref}`,
          `Creativity: ${creativityPref}`,
          `Mathematics: ${mathPref}`,
          `People Interaction: ${peoplePref}`
        ],
        goals,
        constraints,
        programming_preference: programmingPref,
        mathematics_preference: mathPref,
        creativity_level: creativityPref,
        people_interaction_preference: peoplePref
      });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Failed to save profile.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header with Demo fill */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-black text-slate-900 tracking-tight">Student Profile Calibration</h1>
            <p className="text-xs text-slate-500 mt-0.5">Step {step} of 4 &middot; Agentic Profile Synthesis</p>
          </div>
          <button
            onClick={handlePrefillDemo}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-50 text-amber-900 border border-amber-300 hover:bg-amber-100 shadow-sm"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-600" />
            <span>Pre-fill Demo Scenario</span>
          </button>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-200 rounded-full h-2 mb-8 overflow-hidden">
          <div
            className="bg-brand-600 h-full rounded-full transition-all duration-300"
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>

        {error && (
          <div className="mb-6 p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm">
          {/* STEP 1: Academic Background */}
          {step === 1 && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Brain className="w-5 h-5 text-brand-600" />
                <span>Academic Stream & Performance</span>
              </h2>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-2">
                  12th / Intermediate / PUC Stream
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {streamOptions.map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      onClick={() => setStream(opt)}
                      className={`p-3 text-left rounded-xl border text-xs font-semibold transition-all ${
                        stream === opt
                          ? 'border-brand-500 bg-brand-50 text-brand-900 ring-2 ring-brand-500/20'
                          : 'border-slate-200 hover:border-slate-300 text-slate-700'
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Approximate 12th / PUC Percentage ({marksPercentage}%)
                </label>
                <input
                  type="range"
                  min={45}
                  max={100}
                  value={marksPercentage}
                  onChange={(e) => setMarksPercentage(Number(e.target.value))}
                  className="w-full accent-brand-600"
                />
                <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                  <span>Pass (45%)</span>
                  <span>75%</span>
                  <span>Top Distinction (100%)</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Favorite Subjects (comma separated)
                </label>
                <input
                  type="text"
                  value={favoriteSubjects.join(', ')}
                  onChange={(e) => setFavoriteSubjects(e.target.value.split(',').map((s) => s.trim()))}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                  placeholder="Mathematics, Computer Science, English"
                />
              </div>
            </div>
          )}

          {/* STEP 2: Interests & Domains */}
          {step === 2 && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-brand-600" />
                <span>Interests & Discovery Curiosities</span>
              </h2>
              <p className="text-xs text-slate-600">
                Select the broad sectors you find exciting. DISHA uses these to uncover both direct and non-obvious career pathways.
              </p>

              <div className="flex flex-wrap gap-2">
                {interestOptions.map((item) => {
                  const selected = interests.includes(item);
                  return (
                    <button
                      key={item}
                      type="button"
                      onClick={() => toggleInterest(item)}
                      className={`inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all ${
                        selected
                          ? 'bg-brand-600 text-white border-brand-600 shadow-sm'
                          : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {selected && <Check className="w-3.5 h-3.5" />}
                      <span>{item}</span>
                    </button>
                  );
                })}
              </div>

              {/* Skills rating */}
              <div className="pt-4 border-t border-slate-100">
                <h3 className="text-xs font-bold text-slate-900 mb-3 uppercase tracking-wider">
                  Self-Assessed Skill Strengths (1-5)
                </h3>
                <div className="space-y-3">
                  {skills.map((s, idx) => (
                    <div key={idx} className="flex items-center justify-between gap-4">
                      <span className="text-xs font-medium text-slate-700 w-36 truncate">{s.skill}</span>
                      <div className="flex items-center gap-1">
                        {[1, 2, 3, 4, 5].map((level) => (
                          <button
                            key={level}
                            type="button"
                            onClick={() => {
                              const updated = [...skills];
                              updated[idx].level = level;
                              setSkills(updated);
                            }}
                            className={`w-7 h-7 rounded-lg text-xs font-bold transition-all ${
                              s.level >= level
                                ? 'bg-brand-600 text-white'
                                : 'bg-slate-100 text-slate-400 hover:bg-slate-200'
                            }`}
                          >
                            {level}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: Calibration Sliders */}
          {step === 3 && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Sliders className="w-5 h-5 text-brand-600" />
                <span>Decision Preferences & Constraints</span>
              </h2>
              <p className="text-xs text-slate-600">
                Calibrate your preferences honestly. There are no right or wrong choices.
              </p>

              {/* Programming Preference */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <div className="flex justify-between items-center mb-2">
                  <label className="text-xs font-bold text-slate-900">Programming / Coding Intensity</label>
                  <span className="text-xs font-bold text-brand-600 uppercase">{programmingPref}</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5">
                  {(['none', 'low', 'moderate', 'high'] as const).map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => setProgrammingPref(lvl)}
                      className={`py-2 text-center rounded-lg text-xs font-semibold capitalize border ${
                        programmingPref === lvl
                          ? 'bg-brand-600 text-white border-brand-600 shadow-sm'
                          : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {lvl}
                    </button>
                  ))}
                </div>
                <p className="text-[11px] text-slate-500 mt-2">
                  {programmingPref === 'none' || programmingPref === 'low'
                    ? 'DISHA will prioritize human factors, design, research, or managerial technology paths.'
                    : 'DISHA will include software engineering, firmware, and deep systems coding roles.'}
                </p>
              </div>

              {/* Creativity Level */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <div className="flex justify-between items-center mb-2">
                  <label className="text-xs font-bold text-slate-900">Artistic & Creative Engagement</label>
                  <span className="text-xs font-bold text-brand-600 uppercase">{creativityPref}</span>
                </div>
                <div className="grid grid-cols-3 gap-1.5">
                  {(['low', 'moderate', 'high'] as const).map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => setCreativityPref(lvl)}
                      className={`py-2 text-center rounded-lg text-xs font-semibold capitalize border ${
                        creativityPref === lvl
                          ? 'bg-brand-600 text-white border-brand-600 shadow-sm'
                          : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {lvl}
                    </button>
                  ))}
                </div>
              </div>

              {/* Mathematics Comfort */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <div className="flex justify-between items-center mb-2">
                  <label className="text-xs font-bold text-slate-900">Advanced Mathematics Willingness</label>
                  <span className="text-xs font-bold text-brand-600 uppercase">{mathPref}</span>
                </div>
                <div className="grid grid-cols-3 gap-1.5">
                  {(['low', 'moderate', 'high'] as const).map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => setMathPref(lvl)}
                      className={`py-2 text-center rounded-lg text-xs font-semibold capitalize border ${
                        mathPref === lvl
                          ? 'bg-brand-600 text-white border-brand-600 shadow-sm'
                          : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {lvl}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* STEP 4: Goals & Review */}
          {step === 4 && (
            <div className="space-y-6">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Target className="w-5 h-5 text-brand-600" />
                <span>Goals & Horizon Strategy</span>
              </h2>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Primary Goals (e.g. Higher studies, immediate job, creative entrepreneurship)
                </label>
                <input
                  type="text"
                  value={goals.join(', ')}
                  onChange={(e) => setGoals(e.target.value.split(',').map((g) => g.trim()))}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                />
              </div>

              {/* Profile Synthesis Preview Box */}
              <div className="p-4 rounded-xl bg-brand-50/60 border border-brand-200 space-y-2">
                <h4 className="text-xs font-bold text-brand-900 uppercase tracking-wider">
                  Summary Synthesis Preview
                </h4>
                <p className="text-xs text-brand-800 leading-relaxed">
                  <strong>Stream:</strong> {stream} &middot; <strong>Interests:</strong> {interests.join(', ')}
                </p>
                <p className="text-xs text-brand-800 leading-relaxed">
                  <strong>Calibrations:</strong> {programmingPref} programming &middot; {creativityPref} creativity &middot; {mathPref} mathematics
                </p>
                <p className="text-[11px] text-brand-600 pt-1">
                  Profile Agent will normalize these parameters into a structured archetype and run diversity-aware scoring across all 118 career nodes.
                </p>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="mt-8 pt-4 border-t border-slate-100 flex items-center justify-between">
            {step > 1 ? (
              <button
                type="button"
                onClick={() => setStep(step - 1)}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </button>
            ) : <div />}

            {step < 4 ? (
              <button
                type="button"
                onClick={() => setStep(step + 1)}
                className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-lg text-xs font-bold bg-brand-600 hover:bg-brand-700 text-white shadow-sm transition-colors"
              >
                <span>Continue</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSubmit}
                disabled={loading}
                className="inline-flex items-center gap-1.5 px-6 py-2.5 rounded-lg text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition-colors disabled:opacity-50"
              >
                <span>{loading ? 'Synthesizing Profile...' : 'Complete Profile & Explore Careers'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
