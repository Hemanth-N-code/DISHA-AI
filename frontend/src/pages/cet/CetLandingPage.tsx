// frontend/src/pages/cet/CetLandingPage.tsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  GraduationCap, Search, CheckCircle2, AlertTriangle, ArrowRight,
  Sparkles, Compass, ShieldAlert, Award, TrendingUp, Building2, MapPin
} from 'lucide-react';
import { api } from '../../services/api';

const BRANCH_OPTIONS = [
  { code: 'CS', name: 'Computer Science & Engineering' },
  { code: 'IS', name: 'Information Science & Engineering' },
  { code: 'AI', name: 'Artificial Intelligence & ML' },
  { code: 'EC', name: 'Electronics & Communication' },
  { code: 'EE', name: 'Electrical & Electronics' },
  { code: 'ME', name: 'Mechanical Engineering' },
  { code: 'CV', name: 'Civil Engineering' },
  { code: 'BT', name: 'Biotechnology' },
];

const LOCATION_OPTIONS = ['Bengaluru', 'Mysuru', 'Hubballi', 'Mangaluru', 'Belagavi', 'Tumakuru'];
const CATEGORY_OPTIONS = ['GM', '2A', '2B', '3A', '3B', 'SC', 'ST'];

const POPULAR_CAREER_BRIDGES = [
  {
    career: 'Data Scientist & AI Specialist',
    branches: ['Computer Science (CS)', 'Artificial Intelligence & ML (AI)', 'Information Science (IS)'],
    reason: 'Heavy focus on algorithms, linear algebra, distributed computing, and model training.',
  },
  {
    career: 'VLSI & Chip Design Engineer',
    branches: ['Electronics & Communication (EC)', 'Electrical & Electronics (EE)'],
    reason: 'Direct foundation in semiconductor physics, digital systems, CMOS architecture, and FPGA.',
  },
  {
    career: 'Cloud Solutions Architect',
    branches: ['Computer Science (CS)', 'Information Science (IS)'],
    reason: 'Deep coverage of distributed operating systems, containerization, networks, and cyber security.',
  },
  {
    career: 'Robotics & Autonomous Systems',
    branches: ['Electronics & Communication (EC)', 'Mechanical (ME)', 'Computer Science (CS)'],
    reason: 'Interdisciplinary junction of control theory, embedded sensors, kinematics, and computer vision.',
  },
];

export const CetLandingPage: React.FC = () => {
  const navigate = useNavigate();

  // Form State
  const [rank, setRank] = useState<number | ''>(28000);
  const [category, setCategory] = useState<string>('2A');
  const [subCategory, setSubCategory] = useState<string>('General');
  const [gender, setGender] = useState<string>('All');
  const [selectedBranches, setSelectedBranches] = useState<string[]>(['CS', 'IS', 'AI', 'EC']);
  const [selectedLocations, setSelectedLocations] = useState<string[]>(['Bengaluru']);
  const [priority, setPriority] = useState<string>('placements');
  const [loading, setLoading] = useState<boolean>(false);

  const toggleBranch = (code: string) => {
    if (selectedBranches.includes(code)) {
      setSelectedBranches(selectedBranches.filter((b) => b !== code));
    } else {
      setSelectedBranches([...selectedBranches, code]);
    }
  };

  const toggleLocation = (loc: string) => {
    if (selectedLocations.includes(loc)) {
      setSelectedLocations(selectedLocations.filter((l) => l !== loc));
    } else {
      setSelectedLocations([...selectedLocations, loc]);
    }
  };

  const handlePreFillDemo = () => {
    setRank(28000);
    setCategory('2A');
    setSubCategory('General');
    setGender('All');
    setSelectedBranches(['CS', 'IS', 'AI', 'EC']);
    setSelectedLocations(['Bengaluru']);
    setPriority('placements');
  };

  const handleExplore = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!rank || Number(rank) <= 0) return;

    setLoading(true);
    try {
      const token = localStorage.getItem('disha_token');
      if (token) {
        await api.cet.saveProfile({
          exam_id: 'kcet',
          domain_id: 'engineering',
          rank: Number(rank),
          category,
          sub_category: subCategory,
          gender,
          preferred_branches: selectedBranches,
          preferred_locations: selectedLocations,
          preferences: [priority],
        }).catch(() => {});
      }

      await api.cet.logEvent('cet_exploration_initiated', {
        rank: Number(rank),
        category,
        branches: selectedBranches,
        locations: selectedLocations,
      }).catch(() => {});

      const params = new URLSearchParams({
        rank: String(rank),
        category,
        round: '1',
        branches: selectedBranches.join(','),
        locations: selectedLocations.join(','),
      });
      navigate(`/cet/explore?${params.toString()}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      {/* Top Hero Section */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-xs font-semibold">
          <GraduationCap className="w-4 h-4 text-brand-600" />
          <span>CET-Support Engine • Karnataka KCET & KEA Counselling</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Navigate Option Entry with Real Multi-Year Cutoffs
        </h1>
        <p className="text-base text-slate-600 leading-relaxed">
          Transform your KCET rank into an informed, data-driven college preference list. Compare historical
          cutoffs across 2023–2025, verify campus placements, and organize your dream options safely.
        </p>
      </div>

      {/* Mandatory Official Disclaimer Box */}
      <div className="bg-amber-50/80 border border-amber-300/80 rounded-2xl p-5 flex items-start gap-4 shadow-sm">
        <ShieldAlert className="w-6 h-6 text-amber-700 flex-shrink-0 mt-0.5" />
        <div className="space-y-1 text-xs text-amber-950 leading-relaxed">
          <p className="font-bold text-amber-900 text-sm">
            Official Advisory & Historical Data Notice
          </p>
          <p>
            Historical cutoff data is strictly indicative and non-binding. Actual allotment depends on the current year’s
            cutoffs, candidate seat availability, category, course, round, reservation rules, and KEA counselling regulations.
            <strong> DISHA AI does not guarantee admission</strong> to any institution. All figures are verified against official KEA reports.
          </p>
        </div>
      </div>

      {/* Main Grid: Form on Left, Quick Career Bridges on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Calibration Form */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Enter Your CET Details</h2>
              <p className="text-xs text-slate-500 mt-0.5">Calibrate historical cutoffs against your rank</p>
            </div>
            <button
              type="button"
              onClick={handlePreFillDemo}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200 hover:bg-indigo-100 transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
              <span>Demo Profile (Rank 28k)</span>
            </button>
          </div>

          <form onSubmit={handleExplore} className="space-y-5">
            {/* Exam & Domain (Read-only for KCET v1) */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Entrance Examination
                </label>
                <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 flex items-center justify-between">
                  <span>Karnataka KCET (KEA)</span>
                  <span className="text-[10px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded">Active</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Course Domain
                </label>
                <div className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700">
                  Engineering & Technology (B.E / B.Tech)
                </div>
              </div>
            </div>

            {/* Rank & Category */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  KCET Rank <span className="text-rose-500">*</span>
                </label>
                <input
                  type="number"
                  min="1"
                  max="500000"
                  required
                  value={rank}
                  onChange={(e) => setRank(e.target.value ? Number(e.target.value) : '')}
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
                  placeholder="e.g. 28000"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Seat Category
                </label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
                >
                  {CATEGORY_OPTIONS.map((cat) => (
                    <option key={cat} value={cat}>
                      {cat} {cat === 'GM' ? '(General Merit)' : `(Category ${cat})`}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Sub-Category / Quota
                </label>
                <select
                  value={subCategory}
                  onChange={(e) => setSubCategory(e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-brand-500"
                >
                  <option value="General">General / No Special Quota</option>
                  <option value="Rural">Rural Candidate (R)</option>
                  <option value="Kannada">Kannada Medium (K)</option>
                  <option value="HK">Kalyana-Karnataka (371J)</option>
                </select>
              </div>
            </div>

            {/* Preferred Branches */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-slate-700">
                  Preferred Branches ({selectedBranches.length} selected)
                </label>
                <button
                  type="button"
                  onClick={() => setSelectedBranches(BRANCH_OPTIONS.map((b) => b.code))}
                  className="text-[11px] text-brand-600 hover:text-brand-700 font-medium"
                >
                  Select All
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {BRANCH_OPTIONS.map((branch) => {
                  const isSelected = selectedBranches.includes(branch.code);
                  return (
                    <button
                      key={branch.code}
                      type="button"
                      onClick={() => toggleBranch(branch.code)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                        isSelected
                          ? 'bg-brand-50 border-brand-300 text-brand-800 font-semibold shadow-xs'
                          : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      {branch.code} — {branch.name}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Preferred Locations */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-slate-700">
                  Target Locations ({selectedLocations.length} selected)
                </label>
                <button
                  type="button"
                  onClick={() => setSelectedLocations(LOCATION_OPTIONS)}
                  className="text-[11px] text-brand-600 hover:text-brand-700 font-medium"
                >
                  All Karnataka
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {LOCATION_OPTIONS.map((loc) => {
                  const isSelected = selectedLocations.includes(loc);
                  return (
                    <button
                      key={loc}
                      type="button"
                      onClick={() => toggleLocation(loc)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-medium border transition-all flex items-center gap-1.5 ${
                        isSelected
                          ? 'bg-indigo-50 border-indigo-300 text-indigo-800 font-semibold shadow-xs'
                          : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      <MapPin className="w-3 h-3 text-slate-400" />
                      <span>{loc}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Student Preference Priority */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-2">
                Your Primary Priority
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {[
                  { id: 'placements', label: 'Top Placements' },
                  { id: 'branch', label: 'Branch Over College' },
                  { id: 'location', label: 'Metro Location' },
                  { id: 'fees', label: 'Affordable Fees' },
                ].map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => setPriority(p.id)}
                    className={`py-2 px-2.5 rounded-xl text-xs font-semibold border text-center transition-all ${
                      priority === p.id
                        ? 'bg-brand-600 border-brand-600 text-white shadow-sm'
                        : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    {p.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-3">
              <button
                type="submit"
                disabled={loading || !rank || selectedBranches.length === 0}
                className="w-full py-3 px-4 rounded-xl bg-brand-600 hover:bg-brand-700 disabled:bg-slate-300 text-white font-bold text-sm flex items-center justify-center gap-2 shadow-sm transition-all"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Analyzing Historical Data...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Explore Compatible Colleges & Cutoffs</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Right Column: "I Don't Know My Branch Yet" & Popular Bridges */}
        <div className="lg:col-span-5 space-y-6">
          {/* Card 1: Bridge from Careers to Branches */}
          <div className="bg-gradient-to-br from-indigo-900 via-slate-900 to-brand-950 rounded-2xl text-white p-6 shadow-md space-y-4">
            <div className="flex items-center gap-2 text-indigo-300 text-xs font-bold uppercase tracking-wider">
              <Compass className="w-4 h-4" />
              <span>Career &rarr; Academic Branch Bridge</span>
            </div>
            <h3 className="text-xl font-bold leading-tight">
              Unsure which engineering branch to pick?
            </h3>
            <p className="text-xs text-indigo-100/80 leading-relaxed">
              In DISHA AI, careers drive academic choices—not just cutoff ranks. Discover your target future role in our
              118-career universe, and we will reveal exactly which undergraduate branches unlock that path.
            </p>
            <div className="pt-2 flex flex-col sm:flex-row gap-3">
              <Link
                to="/discover"
                className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-white text-slate-900 font-bold text-xs hover:bg-indigo-50 transition-colors"
              >
                <span>Explore Careers Universe</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
              <Link
                to="/what-if"
                className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-indigo-800/60 border border-indigo-600/50 text-indigo-100 font-semibold text-xs hover:bg-indigo-800 transition-colors"
              >
                <span>Try What-If Simulator</span>
              </Link>
            </div>
          </div>

          {/* Card 2: Popular Career-to-Branch Mappings */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-brand-600" />
                <span>Modern Career &rarr; Branch Maps</span>
              </h4>
              <span className="text-[11px] text-slate-400 font-medium">Curated Pathways</span>
            </div>

            <div className="space-y-3">
              {POPULAR_CAREER_BRIDGES.map((bridge, idx) => (
                <div key={idx} className="p-3 bg-slate-50 border border-slate-100 rounded-xl space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900">{bridge.career}</span>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {bridge.branches.map((b, bIdx) => (
                      <span
                        key={bIdx}
                        className="px-2 py-0.5 rounded text-[10px] font-semibold bg-brand-50 text-brand-700 border border-brand-200"
                      >
                        {b}
                      </span>
                    ))}
                  </div>
                  <p className="text-[11px] text-slate-500 italic pt-1">{bridge.reason}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Card 3: Direct Links to Option Builder & Comparisons */}
          <div className="p-4 bg-slate-100/80 border border-slate-200 rounded-xl flex items-center justify-between">
            <div className="space-y-0.5">
              <p className="text-xs font-bold text-slate-800">Have a saved option list?</p>
              <p className="text-[11px] text-slate-500">Reorder your choices or print your final sheet</p>
            </div>
            <Link
              to="/cet/option-list"
              className="px-3 py-1.5 rounded-lg bg-white border border-slate-300 text-slate-800 text-xs font-bold hover:bg-slate-50 shadow-xs"
            >
              My Option List &rarr;
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
