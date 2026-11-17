// frontend/src/pages/cet/CetCollegeDetailPage.tsx
import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, Link } from 'react-router-dom';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ReferenceLine, Legend
} from 'recharts';
import {
  GraduationCap, Building2, MapPin, Globe, Award, TrendingUp,
  ShieldAlert, CheckCircle2, Plus, Check, ArrowLeft, Briefcase, Info, ExternalLink
} from 'lucide-react';
import { api } from '../../services/api';
import { CollegeDetail, CutoffTrendResponse, StudentCetProfile } from '../../types';

export const CetCollegeDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [searchParams, setSearchParams] = useSearchParams();

  const initialBranch = searchParams.get('branch') || 'CS';
  const initialCategory = searchParams.get('category') || 'GM';
  const initialRound = Number(searchParams.get('round')) || 1;

  const [college, setCollege] = useState<CollegeDetail | null>(null);
  const [trend, setTrend] = useState<CutoffTrendResponse | null>(null);
  const [profile, setProfile] = useState<StudentCetProfile | null>(null);

  const [selectedBranch, setSelectedBranch] = useState<string>(initialBranch);
  const [selectedCategory, setSelectedCategory] = useState<string>(initialCategory);
  const [selectedRound, setSelectedRound] = useState<number>(initialRound);

  const [loading, setLoading] = useState<boolean>(true);
  const [trendLoading, setTrendLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [addedBranches, setAddedBranches] = useState<number[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  // Load college and student profile
  useEffect(() => {
    if (!id) return;
    const fetchInitial = async () => {
      setLoading(true);
      try {
        const [colData, profData] = await Promise.all([
          api.cet.getCollegeDetail(id),
          api.cet.getProfile().catch(() => null),
        ]);
        setCollege(colData);
        if (profData) {
          setProfile(profData);
          if (!searchParams.get('category')) {
            setSelectedCategory(profData.category);
          }
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load college details');
      } finally {
        setLoading(false);
      }
    };
    fetchInitial();
  }, [id]);

  // Load trend data whenever branch, category, or round changes
  useEffect(() => {
    if (!id) return;
    const fetchTrend = async () => {
      setTrendLoading(true);
      try {
        const trendData = await api.cet.getCutoffTrend(id, selectedBranch, selectedCategory, selectedRound);
        setTrend(trendData);
      } catch (err: any) {
        console.error('Failed to load cutoff trend', err);
      } finally {
        setTrendLoading(false);
      }
    };
    fetchTrend();
  }, [id, selectedBranch, selectedCategory, selectedRound]);

  const handleAddBranchToOptionList = async (branchId: number, branchName: string) => {
    try {
      await api.cet.addOptionItem({
        college_branch_id: branchId,
        historical_category: 'Historically Compatible',
        student_notes: `Added from college detail: ${college?.short_name} - ${branchName}`,
      });
      setAddedBranches((prev) => [...prev, branchId]);
      showToast(`Added ${branchName} at ${college?.short_name} to your Option Entry List!`);
    } catch (err: any) {
      showToast(err.message || 'Please log in to save options.');
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm font-semibold text-slate-700">Loading College Profile...</p>
      </div>
    );
  }

  if (error || !college) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
        <ShieldAlert className="w-12 h-12 text-rose-500 mx-auto" />
        <h2 className="text-2xl font-bold text-slate-900">College Not Found</h2>
        <p className="text-sm text-slate-500">{error || 'Unable to retrieve college details.'}</p>
        <Link to="/cet/explore" className="px-4 py-2 bg-brand-600 text-white rounded-xl text-xs font-bold inline-block">
          Back to Explorer
        </Link>
      </div>
    );
  }

  // Trend chart data mapping
  const chartData = (trend?.trend_points || []).map((pt) => ({
    year: String(pt.year),
    closing_rank: pt.closing_rank,
    category: pt.category,
    round: pt.round,
  }));

  const studentRank = profile?.rank || 28000;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Toast */}
      {toastMessage && (
        <div className="fixed top-20 right-6 z-50 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-xl text-xs font-semibold flex items-center gap-2 border border-slate-700 animate-fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Back Link */}
      <Link
        to="/cet/explore"
        className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to CET Explorer</span>
      </Link>

      {/* College Header Profile */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-2.5 py-1 bg-brand-100 text-brand-800 rounded-lg text-xs font-black">
                KEA CODE: {college.code}
              </span>
              <span className="px-2.5 py-1 bg-slate-100 text-slate-700 rounded-lg text-xs font-bold">
                {college.college_type}
              </span>
              {college.accreditation && (
                <span className="px-2.5 py-1 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-lg text-xs font-semibold flex items-center gap-1">
                  <Award className="w-3.5 h-3.5" />
                  <span>{college.accreditation}</span>
                </span>
              )}
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">{college.name}</h1>
            <p className="text-xs text-slate-500 flex items-center gap-2">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              <span>{college.location}, {college.city}, {college.district}</span>
              {college.established_year && (
                <>
                  <span>•</span>
                  <span>Est. {college.established_year}</span>
                </>
              )}
            </p>
          </div>

          <div className="flex items-center gap-3">
            {college.website && (
              <a
                href={college.website}
                target="_blank"
                rel="noreferrer"
                className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors"
              >
                <Globe className="w-3.5 h-3.5" />
                <span>Official Website</span>
                <ExternalLink className="w-3 h-3 text-slate-400" />
              </a>
            )}
          </div>
        </div>

        {college.description && (
          <p className="text-xs text-slate-600 leading-relaxed border-t border-slate-100 pt-4">
            {college.description}
          </p>
        )}

        {/* Quick Highlights Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 border-t border-slate-100 pt-4">
          <div className="p-3 bg-slate-50 rounded-xl">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Campus Area</span>
            <span className="text-sm font-extrabold text-slate-800">
              {college.campus_area_acres ? `${college.campus_area_acres} Acres` : 'N/A'}
            </span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Hostel Facility</span>
            <span className="text-sm font-extrabold text-slate-800">
              {college.hostel_facility ? 'Available (Boys & Girls)' : 'Day Scholar Only'}
            </span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Total Branches</span>
            <span className="text-sm font-extrabold text-slate-800">{college.branches.length} Programs</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl">
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Data Authority</span>
            <span className="text-sm font-extrabold text-emerald-700">{college.source}</span>
          </div>
        </div>
      </div>

      {/* Verified Placement Statistics */}
      {college.placement && (
        <div className="bg-gradient-to-r from-indigo-900 to-slate-900 text-white rounded-2xl p-6 shadow-md space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-indigo-800/80 pb-3">
            <div className="flex items-center gap-2">
              <Briefcase className="w-5 h-5 text-indigo-300" />
              <h2 className="text-base font-bold">Official Campus Placement Statistics ({college.placement.year})</h2>
            </div>
            <div className="flex items-center gap-2 text-xs text-indigo-300">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Source: {college.placement.source} (Verified)</span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="p-3.5 bg-indigo-800/40 rounded-xl border border-indigo-700/40">
              <span className="text-[10px] uppercase tracking-wider text-indigo-300 block">Median CTC</span>
              <span className="text-2xl font-black text-white">
                {college.placement.median_package_lpa ? `₹${college.placement.median_package_lpa} LPA` : 'N/A'}
              </span>
            </div>
            <div className="p-3.5 bg-indigo-800/40 rounded-xl border border-indigo-700/40">
              <span className="text-[10px] uppercase tracking-wider text-indigo-300 block">Average CTC</span>
              <span className="text-2xl font-black text-white">
                {college.placement.average_package_lpa ? `₹${college.placement.average_package_lpa} LPA` : 'N/A'}
              </span>
            </div>
            <div className="p-3.5 bg-indigo-800/40 rounded-xl border border-indigo-700/40">
              <span className="text-[10px] uppercase tracking-wider text-indigo-300 block">Highest CTC</span>
              <span className="text-2xl font-black text-emerald-400">
                {college.placement.highest_package_lpa ? `₹${college.placement.highest_package_lpa} LPA` : 'N/A'}
              </span>
            </div>
            <div className="p-3.5 bg-indigo-800/40 rounded-xl border border-indigo-700/40">
              <span className="text-[10px] uppercase tracking-wider text-indigo-300 block">Placement Rate</span>
              <span className="text-2xl font-black text-white">
                {college.placement.placement_rate ? `${college.placement.placement_rate}%` : 'N/A'}
              </span>
            </div>
          </div>

          {college.placement.top_recruiters && college.placement.top_recruiters.length > 0 && (
            <div className="pt-2">
              <span className="text-xs text-indigo-200 font-semibold block mb-2">Key Campus Recruiters:</span>
              <div className="flex flex-wrap gap-2">
                {college.placement.top_recruiters.map((rec, i) => (
                  <span
                    key={i}
                    className="px-2.5 py-1 bg-white/10 rounded-lg text-xs font-semibold text-indigo-100 border border-white/10"
                  >
                    {rec}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Multi-Year Cutoff Trend Interactive Chart */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-brand-600" />
              <span>Multi-Year Cutoff Trend Analysis</span>
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Historical closing rank evolution with your horizontal rank reference benchmark
            </p>
          </div>

          {/* Interactive Chart Controls */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Branch Selector */}
            <div>
              <label className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">Branch</label>
              <select
                value={selectedBranch}
                onChange={(e) => setSelectedBranch(e.target.value)}
                className="text-xs font-bold bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-800"
              >
                {college.branches.map((b) => (
                  <option key={b.branch_code} value={b.branch_code}>
                    {b.branch_code} — {b.branch_name}
                  </option>
                ))}
              </select>
            </div>

            {/* Category Selector */}
            <div>
              <label className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">Category</label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="text-xs font-bold bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-800"
              >
                {['GM', '2A', '2B', '3A', '3B', 'SC', 'ST'].map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            {/* Round Selector */}
            <div>
              <label className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">KEA Round</label>
              <select
                value={selectedRound}
                onChange={(e) => setSelectedRound(Number(e.target.value))}
                className="text-xs font-bold bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-800"
              >
                <option value={1}>Round 1</option>
                <option value={2}>Round 2</option>
              </select>
            </div>
          </div>
        </div>

        {/* Direction Badge */}
        {trend && (
          <div className="flex items-center justify-between text-xs bg-slate-50 p-3 rounded-xl border border-slate-100">
            <div className="flex items-center gap-2">
              <Info className="w-4 h-4 text-brand-600" />
              <span className="text-slate-700">
                Cutoff Pattern: <strong>{trend.direction.replace('_', ' ')}</strong> for branch{' '}
                <strong>{selectedBranch}</strong> under category <strong>{selectedCategory}</strong>
              </span>
            </div>
            <span className="text-[11px] font-semibold text-slate-500">
              Years Covered: {trend.available_years.join(', ')}
            </span>
          </div>
        )}

        {/* Recharts Component */}
        <div className="h-72 w-full pt-4">
          {trendLoading ? (
            <div className="h-full flex items-center justify-center">
              <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 12, fontWeight: 600 }} />
                <YAxis
                  stroke="#64748b"
                  domain={['auto', 'auto']}
                  tick={{ fontSize: 11 }}
                  tickFormatter={(val) => val.toLocaleString()}
                />
                <Tooltip
                  formatter={(val: any) => [`Rank: ${Number(val).toLocaleString()}`, 'Closing Rank']}
                  labelFormatter={(lbl) => `Year ${lbl} (KEA Round ${selectedRound})`}
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderRadius: '12px',
                    color: '#fff',
                    border: 'none',
                    fontSize: '12px',
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Line
                  type="monotone"
                  dataKey="closing_rank"
                  name={`${college.short_name} Cutoff (${selectedBranch})`}
                  stroke="#2563eb"
                  strokeWidth={3}
                  activeDot={{ r: 8 }}
                  dot={{ r: 5, fill: '#2563eb' }}
                />
                {studentRank > 0 && (
                  <ReferenceLine
                    y={studentRank}
                    stroke="#e11d48"
                    strokeDasharray="4 4"
                    strokeWidth={2}
                    label={{
                      value: `Your KCET Rank: ${studentRank.toLocaleString()}`,
                      fill: '#e11d48',
                      fontSize: 11,
                      fontWeight: 700,
                      position: 'top',
                    }}
                  />
                )}
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-slate-500 italic">
              No historical cutoffs recorded for this branch/category combination.
            </div>
          )}
        </div>
      </div>

      {/* Available Branches Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Active Engineering Branches</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Annual tuition fee benchmarks and option list addition
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 font-bold uppercase text-[10px]">
                <th className="pb-3">Code</th>
                <th className="pb-3">Branch Name</th>
                <th className="pb-3">Annual Intake</th>
                <th className="pb-3">Govt / KEA Tuition Fee</th>
                <th className="pb-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
              {college.branches.map((b) => {
                const isAdded = addedBranches.includes(b.id);
                return (
                  <tr key={b.id} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3 font-extrabold text-brand-700">{b.branch_code}</td>
                    <td className="py-3 font-bold text-slate-900">{b.branch_name}</td>
                    <td className="py-3">{b.intake} seats</td>
                    <td className="py-3 font-semibold text-slate-800">
                      {b.tuition_fee_annual ? `₹${b.tuition_fee_annual.toLocaleString()} / year` : 'As per KEA norms'}
                    </td>
                    <td className="py-3 text-right">
                      <button
                        onClick={() => handleAddBranchToOptionList(b.id, b.branch_name)}
                        className={`px-3 py-1.5 rounded-xl font-bold text-xs inline-flex items-center gap-1 transition-all ${
                          isAdded
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-brand-600 hover:bg-brand-700 text-white shadow-xs'
                        }`}
                      >
                        {isAdded ? (
                          <>
                            <Check className="w-3.5 h-3.5" />
                            <span>Added</span>
                          </>
                        ) : (
                          <>
                            <Plus className="w-3.5 h-3.5" />
                            <span>Add to Option List</span>
                          </>
                        )}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Official Disclaimer */}
      <div className="bg-amber-50/90 border border-amber-300 rounded-xl p-4 flex items-start gap-3 text-xs text-amber-950">
        <ShieldAlert className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Official Disclaimer: </span>
          All cutoffs and placement figures are indicative historical reference records drawn from official KEA and NIRF
          reports. Seat allotment is subject to real-time counselling dynamics. DISHA does not guarantee allotment.
        </div>
      </div>
    </div>
  );
};
