// frontend/src/pages/cet/CetExplorerPage.tsx
import React, { useState, useEffect } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import {
  GraduationCap, Search, Filter, ShieldAlert, ArrowUpDown,
  Building2, CheckCircle2, AlertCircle, Plus, Check, Scale,
  ChevronRight, Sparkles, MapPin, Briefcase, Award, ExternalLink,
  Layers, Compass
} from 'lucide-react';
import { api } from '../../services/api';
import { CetAnalyzeResponse, CetOptionMatchItem } from '../../types';

const REGION_MAP: Record<string, string[]> = {
  Bengaluru: ['Bengaluru'],
  Mysuru: ['Mysuru', 'Mandya'],
  North: ['Hubballi', 'Belagavi', 'Dharwad', 'Bagalkot', 'Vijayapura'],
  Coastal: ['Mangaluru', 'Nitte', 'Moodbidri'],
  Central: ['Tumakuru', 'Hassan', 'Davanagere', 'Shivamogga'],
  HK: ['Kalaburagi', 'Ballari', 'Bhalki'],
};

export const CetExplorerPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const initialRank = Number(searchParams.get('rank')) || 28000;
  const initialCategory = searchParams.get('category') || '2A';
  const initialRound = Number(searchParams.get('round')) || 1;
  const branchesParam = searchParams.get('branches');
  const locationsParam = searchParams.get('locations');

  const [rank, setRank] = useState<number>(initialRank);
  const [category, setCategory] = useState<string>(initialCategory);
  const [roundNum, setRoundNum] = useState<number>(initialRound);
  const [preferredBranches] = useState<string[]>(
    branchesParam ? branchesParam.split(',').filter(Boolean) : []
  );
  const [preferredLocations] = useState<string[]>(
    locationsParam ? locationsParam.split(',').filter(Boolean) : []
  );

  const [loading, setLoading] = useState<boolean>(true);
  const [data, setData] = useState<CetAnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Filters & Sorting Vision
  const [filterMatch, setFilterMatch] = useState<string>('ALL');
  const [filterBranch, setFilterBranch] = useState<string>('ALL');
  const [filterCity, setFilterCity] = useState<string>('ALL');
  const [filterRegion, setFilterRegion] = useState<string>('ALL');
  const [sortBy, setSortBy] = useState<string>('match_score');
  const [visibleCount, setVisibleCount] = useState<number>(24);

  // Interactive state
  const [selectedForCompare, setSelectedForCompare] = useState<string[]>([]);
  const [addedOptionBranchIds, setAddedOptionBranchIds] = useState<number[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.cet.analyzeOptions({
        rank,
        category,
        domain_id: 'engineering',
        preferred_branches: preferredBranches.length > 0 ? preferredBranches : undefined,
        preferred_locations: preferredLocations.length > 0 ? preferredLocations : undefined,
        round_num: roundNum,
        sort_by: sortBy,
      });
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze CET options');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis();
  }, [rank, category, roundNum, sortBy]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  const handleAddToOptionList = async (opt: CetOptionMatchItem) => {
    try {
      await api.cet.addOptionItem({
        college_branch_id: opt.branch_id,
        historical_category: opt.historical_match_label,
        student_notes: `Match score: ${opt.match_score}. 2024 Cutoff: ${opt.most_recent_closing_rank || 'N/A'}`,
      });
      setAddedOptionBranchIds((prev) => [...prev, opt.branch_id]);
      showToast(`Added ${opt.college_short_name} (${opt.branch_code}) to your Option Entry List!`);
    } catch (err: any) {
      showToast(err.message || 'Please log in to save options to your personal list.');
    }
  };

  const toggleCompare = (collegeId: string) => {
    if (selectedForCompare.includes(collegeId)) {
      setSelectedForCompare(selectedForCompare.filter((id) => id !== collegeId));
    } else {
      if (selectedForCompare.length >= 4) {
        showToast('Maximum 4 colleges can be compared simultaneously.');
        return;
      }
      setSelectedForCompare([...selectedForCompare, collegeId]);
    }
  };

  // Filtered Options
  const filteredOptions = (data?.options || []).filter((opt) => {
    if (filterMatch !== 'ALL' && opt.historical_match_label !== filterMatch) return false;
    if (filterBranch !== 'ALL' && opt.branch_code !== filterBranch) return false;
    if (filterCity !== 'ALL' && opt.city !== filterCity) return false;
    if (filterRegion !== 'ALL') {
      const validCities = REGION_MAP[filterRegion] || [];
      if (!validCities.includes(opt.city)) return false;
    }
    return true;
  });

  const uniqueBranches = Array.from(new Set((data?.options || []).map((o) => o.branch_code)));
  const uniqueCities = Array.from(new Set((data?.options || []).map((o) => o.city)));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 right-6 z-50 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-xl text-xs font-semibold flex items-center gap-2 border border-slate-700 animate-fade-in">
          <Sparkles className="w-4 h-4 text-brand-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Top Header & Context */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-brand-700 uppercase tracking-wider mb-1">
            <GraduationCap className="w-4 h-4" />
            <span>KCET Comprehensive Engineering Knowledge Base (55+ Colleges)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            College & Course Decision Vision
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Giving you the full vision—not deciding for you. Review historical cutoffs, verified placements, and choose your path.
          </p>
        </div>

        {/* Quick Calibration Bar */}
        <div className="flex items-center gap-3 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
          <div className="px-3 py-1 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Your Rank</span>
            <span className="text-sm font-extrabold text-brand-700">{rank.toLocaleString()}</span>
          </div>
          <div className="px-3 py-1 bg-slate-50 rounded-xl border border-slate-100">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Category</span>
            <span className="text-sm font-extrabold text-slate-800">{category}</span>
          </div>
          <div className="px-2">
            <span className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">Round</span>
            <select
              value={roundNum}
              onChange={(e) => setRoundNum(Number(e.target.value))}
              className="text-xs font-bold bg-white border border-slate-200 rounded-lg px-2 py-1 text-slate-700"
            >
              <option value={1}>Round 1</option>
              <option value={2}>Round 2</option>
            </select>
          </div>
          <Link
            to="/cet"
            className="text-xs font-semibold text-brand-600 hover:text-brand-700 px-3 py-1.5 rounded-xl hover:bg-brand-50"
          >
            Edit
          </Link>
        </div>
      </div>

      {/* Mandatory Disclaimer */}
      <div className="bg-amber-50/90 border border-amber-300 rounded-xl p-4 flex items-start gap-3 text-xs text-amber-950">
        <ShieldAlert className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Historical Cutoff Disclaimer: </span>
          {data?.disclaimer ||
            "Historical cutoff data is strictly indicative. Actual allotment depends on current year cutoffs, seat availability, category, course, and KEA counselling rules. DISHA gives you the vision to choose, not an admission guarantee."}
        </div>
      </div>

      {/* Summary Stat Cards */}
      {data && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <button
            onClick={() => setFilterMatch('ALL')}
            className={`p-3.5 rounded-2xl border text-left transition-all ${
              filterMatch === 'ALL'
                ? 'bg-slate-900 text-white border-slate-900 shadow-sm'
                : 'bg-white text-slate-800 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <span className="text-[10px] uppercase font-bold block opacity-70">Total Options</span>
            <span className="text-2xl font-black">{data.total_options_evaluated}</span>
            <span className="text-[11px] block mt-1">Across 55+ Colleges</span>
          </button>

          <button
            onClick={() => setFilterMatch('Strong historical match')}
            className={`p-3.5 rounded-2xl border text-left transition-all ${
              filterMatch === 'Strong historical match'
                ? 'bg-emerald-600 text-white border-emerald-600 shadow-sm'
                : 'bg-white text-slate-800 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <span className="text-[10px] uppercase font-bold block text-emerald-600">High Match</span>
            <span className="text-2xl font-black text-emerald-700">{data.strong_matches_count}</span>
            <span className="text-[11px] block text-slate-500 mt-1">Strong Match</span>
          </button>

          <button
            onClick={() => setFilterMatch('Possible match')}
            className={`p-3.5 rounded-2xl border text-left transition-all ${
              filterMatch === 'Possible match'
                ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                : 'bg-white text-slate-800 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <span className="text-[10px] uppercase font-bold block text-blue-600">Borderline</span>
            <span className="text-2xl font-black text-blue-700">{data.possible_matches_count}</span>
            <span className="text-[11px] block text-slate-500 mt-1">Possible Match</span>
          </button>

          <button
            onClick={() => setFilterMatch('Lower historical cutoff / safer option')}
            className={`p-3.5 rounded-2xl border text-left transition-all ${
              filterMatch === 'Lower historical cutoff / safer option'
                ? 'bg-purple-600 text-white border-purple-600 shadow-sm'
                : 'bg-white text-slate-800 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <span className="text-[10px] uppercase font-bold block text-purple-600">Safety Cushion</span>
            <span className="text-2xl font-black text-purple-700">{data.safer_matches_count}</span>
            <span className="text-[11px] block text-slate-500 mt-1">Safer Options</span>
          </button>

          <button
            onClick={() => setFilterMatch('Competitive option')}
            className={`p-3.5 rounded-2xl border text-left transition-all ${
              filterMatch === 'Competitive option'
                ? 'bg-amber-600 text-white border-amber-600 shadow-sm'
                : 'bg-white text-slate-800 border-slate-200 hover:bg-slate-50'
            }`}
          >
            <span className="text-[10px] uppercase font-bold block text-amber-600">Ambitious</span>
            <span className="text-2xl font-black text-amber-700">{data.competitive_matches_count}</span>
            <span className="text-[11px] block text-slate-500 mt-1">Aspirational</span>
          </button>
        </div>
      )}

      {/* Vision & Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex flex-wrap items-center gap-3">
          {/* Sorting Control */}
          <div className="flex items-center gap-1.5">
            <ArrowUpDown className="w-3.5 h-3.5 text-brand-600" />
            <label className="text-xs font-bold text-slate-700">Sort Vision:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="text-xs font-semibold bg-brand-50 text-brand-900 border border-brand-200 rounded-xl px-3 py-1.5"
            >
              <option value="match_score">Balanced Match & Rating</option>
              <option value="placement_desc">Highest Placement CTC (Median)</option>
              <option value="cutoff_asc">Most Competitive Cutoff First</option>
              <option value="cutoff_desc">Safest Historical Cutoff First</option>
            </select>
          </div>

          <div className="h-4 w-px bg-slate-200 hidden sm:block" />

          {/* Region Quick Filter */}
          <div className="flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5 text-slate-500" />
            <select
              value={filterRegion}
              onChange={(e) => {
                setFilterRegion(e.target.value);
                setFilterCity('ALL');
              }}
              className="text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-700"
            >
              <option value="ALL">All Regions (Karnataka)</option>
              <option value="Bengaluru">Bengaluru Hub (30+ Colleges)</option>
              <option value="Mysuru">Mysuru & Mandya</option>
              <option value="North">North Karnataka (Hubballi, Belagavi)</option>
              <option value="Coastal">Coastal Karnataka (Mangaluru, Udupi)</option>
              <option value="Central">Central (Tumakuru, Hassan, Davanagere)</option>
              <option value="HK">Kalyana-Karnataka (Kalaburagi, Ballari)</option>
            </select>
          </div>

          {/* Branch Filter */}
          <select
            value={filterBranch}
            onChange={(e) => setFilterBranch(e.target.value)}
            className="text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-700"
          >
            <option value="ALL">All Branches ({uniqueBranches.length})</option>
            {uniqueBranches.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>

          {/* City Filter */}
          <select
            value={filterCity}
            onChange={(e) => setFilterCity(e.target.value)}
            className="text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-700"
          >
            <option value="ALL">All Cities ({uniqueCities.length})</option>
            {uniqueCities.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        <div className="text-xs text-slate-500 font-medium">
          Showing <strong>{Math.min(visibleCount, filteredOptions.length)}</strong> of <strong>{filteredOptions.length}</strong> matching options
        </div>
      </div>

      {/* Loading & Error States */}
      {loading && (
        <div className="text-center py-20 bg-white rounded-2xl border border-slate-200">
          <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm font-semibold text-slate-700">Evaluating 55+ colleges across Karnataka with real KEA cutoffs...</p>
        </div>
      )}

      {error && (
        <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl text-center space-y-2">
          <AlertCircle className="w-8 h-8 text-rose-600 mx-auto" />
          <p className="text-sm font-bold text-rose-900">{error}</p>
          <button
            onClick={fetchAnalysis}
            className="px-4 py-1.5 bg-rose-600 text-white rounded-xl text-xs font-bold"
          >
            Retry Analysis
          </button>
        </div>
      )}

      {/* Grid of Matched Options */}
      {!loading && !error && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredOptions.slice(0, visibleCount).map((opt) => {
              const isAdded = addedOptionBranchIds.includes(opt.branch_id);
              const isSelectedCompare = selectedForCompare.includes(opt.college_id);

              // Badge styling
              let badgeBg = 'bg-slate-100 text-slate-800 border-slate-200';
              if (opt.match_badge_color === 'green') badgeBg = 'bg-emerald-50 text-emerald-800 border-emerald-300';
              else if (opt.match_badge_color === 'blue') badgeBg = 'bg-blue-50 text-blue-800 border-blue-300';
              else if (opt.match_badge_color === 'purple') badgeBg = 'bg-purple-50 text-purple-800 border-purple-300';
              else if (opt.match_badge_color === 'amber') badgeBg = 'bg-amber-50 text-amber-800 border-amber-300';

              return (
                <div
                  key={`${opt.college_id}-${opt.branch_id}`}
                  className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow p-5 flex flex-col justify-between space-y-4"
                >
                  <div className="space-y-3">
                    {/* Top Row: College Code & Match Badge */}
                    <div className="flex items-start justify-between gap-2">
                      <div className="space-y-0.5">
                        <div className="flex items-center gap-1.5">
                          <span className="text-[10px] font-extrabold bg-slate-100 text-slate-700 px-2 py-0.5 rounded-md border border-slate-200">
                            {opt.college_code}
                          </span>
                          <span className="text-[11px] font-semibold text-slate-500 flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {opt.city}
                          </span>
                        </div>
                        <h3 className="font-bold text-slate-900 text-base leading-snug pt-1">
                          {opt.college_name}
                        </h3>
                      </div>

                      <div className="text-right flex-shrink-0">
                        <span className="text-[11px] font-extrabold text-brand-700 block">
                          Score: {opt.match_score}
                        </span>
                      </div>
                    </div>

                    {/* Branch Pill */}
                    <div className="bg-slate-50 border border-slate-100 rounded-xl p-2.5 flex items-center justify-between">
                      <div>
                        <span className="text-xs font-bold text-slate-900 block">{opt.branch_name}</span>
                        <span className="text-[10px] font-semibold text-slate-500">Branch Code: {opt.branch_code}</span>
                      </div>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-white border border-slate-200 text-slate-700">
                        {opt.college_type}
                      </span>
                    </div>

                    {/* Match Classification Badge */}
                    <div className={`px-2.5 py-1.5 rounded-xl border text-xs font-semibold flex items-center gap-2 ${badgeBg}`}>
                      <CheckCircle2 className="w-3.5 h-3.5 flex-shrink-0" />
                      <span>{opt.historical_match_label}</span>
                    </div>

                    {/* Explanation Snippet */}
                    <p className="text-[11px] text-slate-600 leading-relaxed italic bg-slate-50/70 p-2.5 rounded-xl border border-slate-100">
                      {opt.historical_explanation}
                    </p>

                    {/* Multi-Year Closing Cutoffs Pill Bar */}
                    <div className="border border-slate-100 rounded-xl p-2.5 space-y-1.5">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                        Historical Closing Ranks ({category})
                      </span>
                      <div className="grid grid-cols-3 gap-2 text-center">
                        {[2023, 2024, 2025].map((yr) => (
                          <div key={yr} className="bg-slate-50 p-1 rounded-lg">
                            <span className="text-[10px] text-slate-500 block">{yr}</span>
                            <span className="text-xs font-extrabold text-slate-800">
                              {opt.closing_ranks[yr] ? opt.closing_ranks[yr].toLocaleString() : '—'}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Placement Highlights */}
                    {opt.placement && (
                      <div className="flex items-center justify-between text-xs bg-indigo-50/50 border border-indigo-100 rounded-xl p-2.5">
                        <div>
                          <span className="text-[10px] text-indigo-600 font-bold uppercase block">Median CTC</span>
                          <span className="font-extrabold text-indigo-950">
                            {opt.placement.median_package_lpa ? `₹${opt.placement.median_package_lpa} LPA` : 'N/A'}
                          </span>
                        </div>
                        <div>
                          <span className="text-[10px] text-indigo-600 font-bold uppercase block">Highest CTC</span>
                          <span className="font-extrabold text-indigo-950">
                            {opt.placement.highest_package_lpa ? `₹${opt.placement.highest_package_lpa} LPA` : 'N/A'}
                          </span>
                        </div>
                        <div className="text-right">
                          <span className="text-[9px] text-indigo-500 font-semibold block">{opt.placement.source || 'NIRF'}</span>
                          <span className="text-[10px] text-emerald-700 font-bold">Verified</span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Card Action Buttons */}
                  <div className="pt-2 border-t border-slate-100 space-y-2">
                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => handleAddToOptionList(opt)}
                        className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition-all ${
                          isAdded
                            ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                            : 'bg-brand-600 hover:bg-brand-700 text-white shadow-xs'
                        }`}
                      >
                        {isAdded ? (
                          <>
                            <Check className="w-3.5 h-3.5" />
                            <span>In Option List</span>
                          </>
                        ) : (
                          <>
                            <Plus className="w-3.5 h-3.5" />
                            <span>Add to Option List</span>
                          </>
                        )}
                      </button>

                      <button
                        type="button"
                        onClick={() => toggleCompare(opt.college_id)}
                        className={`py-2 px-3 rounded-xl text-xs font-semibold border flex items-center gap-1 transition-colors ${
                          isSelectedCompare
                            ? 'bg-slate-900 text-white border-slate-900'
                            : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                        }`}
                        title="Select to compare side-by-side"
                      >
                        <Scale className="w-3.5 h-3.5" />
                        <span>{isSelectedCompare ? 'Selected' : 'Compare'}</span>
                      </button>
                    </div>

                    <Link
                      to={`/cet/colleges/${opt.college_id}?branch=${opt.branch_code}&category=${category}`}
                      className="w-full py-1.5 text-center text-xs font-semibold text-brand-700 hover:text-brand-900 flex items-center justify-center gap-1"
                    >
                      <span>View Cutoff Trends & Campus Profile</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Load More Button */}
          {visibleCount < filteredOptions.length && (
            <div className="text-center pt-6 pb-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={() => setVisibleCount((prev) => prev + 24)}
                className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold shadow-sm transition-all flex items-center gap-2"
              >
                <span>Show More Colleges (Showing {Math.min(visibleCount, filteredOptions.length)} of {filteredOptions.length})</span>
              </button>
              <button
                onClick={() => setVisibleCount(filteredOptions.length)}
                className="px-4 py-2.5 bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 rounded-xl text-xs font-semibold"
              >
                Show All ({filteredOptions.length})
              </button>
            </div>
          )}
        </>
      )}

      {/* Floating Compare & Option List Drawer */}
      <div className="sticky bottom-4 z-30 bg-slate-900/95 backdrop-blur text-white rounded-2xl p-4 shadow-2xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-2">
            <Scale className="w-4 h-4 text-brand-400" />
            <span>
              Comparing: <strong>{selectedForCompare.length} / 4</strong> colleges
            </span>
          </div>
          <div className="h-4 w-px bg-slate-700 hidden sm:block" />
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>
              Added to List: <strong>{addedOptionBranchIds.length}</strong> branches
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          {selectedForCompare.length >= 2 && (
            <button
              onClick={() => {
                const ids = selectedForCompare.join(',');
                navigate(`/cet/compare?ids=${ids}&branch=CS&category=${category}`);
              }}
              className="flex-1 sm:flex-none px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition-colors shadow-sm"
            >
              <Scale className="w-3.5 h-3.5" />
              <span>Compare Now ({selectedForCompare.length})</span>
            </button>
          )}

          <Link
            to="/cet/option-list"
            className="flex-1 sm:flex-none px-4 py-2 bg-white text-slate-900 hover:bg-slate-100 rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition-colors"
          >
            <span>Open Option Builder &rarr;</span>
          </Link>
        </div>
      </div>
    </div>
  );
};
