// frontend/src/pages/cet/CetComparisonPage.tsx
import React, { useState, useEffect } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import {
  Scale, ArrowLeft, Building2, MapPin, Award, CheckCircle2,
  ShieldAlert, Plus, Check, Trash2, Briefcase, ExternalLink
} from 'lucide-react';
import { api } from '../../services/api';
import { CollegeComparisonResponse, CollegeDetail } from '../../types';

export const CetComparisonPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const idsParam = searchParams.get('ids') || 'rvce,bmsce,msrit';
  const initialBranch = searchParams.get('branch') || 'CS';
  const initialCategory = searchParams.get('category') || 'GM';

  const [collegeIds, setCollegeIds] = useState<string[]>(idsParam.split(',').filter(Boolean));
  const [branchCode, setBranchCode] = useState<string>(initialBranch);
  const [category, setCategory] = useState<string>(initialCategory);

  const [allColleges, setAllColleges] = useState<CollegeDetail[]>([]);
  const [comparisonData, setComparisonData] = useState<CollegeComparisonResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [addedColleges, setAddedColleges] = useState<string[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  // Load all colleges for dropdown selection
  useEffect(() => {
    api.cet.getColleges().then(setAllColleges).catch(() => {});
  }, []);

  // Fetch comparison
  const fetchComparison = async () => {
    if (collegeIds.length === 0) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.cet.compareColleges({
        college_ids: collegeIds,
        branch_code: branchCode,
        category,
      });
      setComparisonData(res);
    } catch (err: any) {
      setError(err.message || 'Failed to compare colleges');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComparison();
    // Update URL params
    setSearchParams({
      ids: collegeIds.join(','),
      branch: branchCode,
      category,
    });
  }, [collegeIds, branchCode, category]);

  const handleRemoveCollege = (idToRemove: string) => {
    if (collegeIds.length <= 1) {
      showToast('At least 1 college must remain in comparison.');
      return;
    }
    setCollegeIds(collegeIds.filter((id) => id !== idToRemove));
  };

  const handleAddCollege = (idToAdd: string) => {
    if (!idToAdd) return;
    if (collegeIds.includes(idToAdd)) {
      showToast('College already in comparison.');
      return;
    }
    if (collegeIds.length >= 4) {
      showToast('Maximum 4 colleges can be compared at once.');
      return;
    }
    setCollegeIds([...collegeIds, idToAdd]);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 right-6 z-50 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-xl text-xs font-semibold flex items-center gap-2 border border-slate-700 animate-fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <Link
            to="/cet/explore"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 mb-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Explorer</span>
          </Link>
          <div className="flex items-center gap-2 text-xs font-bold text-brand-700 uppercase tracking-wider">
            <Scale className="w-4 h-4" />
            <span>Side-by-Side Evaluation</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            College & Branch Multi-Factor Comparison
          </h1>
        </div>

        {/* Global Controls */}
        <div className="flex flex-wrap items-center gap-3 bg-white p-3 rounded-2xl border border-slate-200 shadow-sm">
          <div>
            <label className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">Branch</label>
            <select
              value={branchCode}
              onChange={(e) => setBranchCode(e.target.value)}
              className="text-xs font-bold bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-800"
            >
              {['CS', 'IS', 'AI', 'EC', 'EE', 'ME', 'CV', 'BT'].map((b) => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="text-xs font-bold bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-slate-800"
            >
              {['GM', '2A', '2B', '3A', '3B', 'SC', 'ST'].map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          {collegeIds.length < 4 && (
            <div>
              <label className="text-[10px] uppercase font-bold text-slate-400 block mb-0.5">Add College</label>
              <select
                onChange={(e) => {
                  handleAddCollege(e.target.value);
                  e.target.value = '';
                }}
                defaultValue=""
                className="text-xs font-bold bg-brand-50 text-brand-800 border border-brand-200 rounded-xl px-3 py-1.5"
              >
                <option value="" disabled>+ Select College...</option>
                {allColleges
                  .filter((c) => !collegeIds.includes(c.id))
                  .sort((a, b) => a.short_name.localeCompare(b.short_name))
                  .map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.short_name} ({c.code}) — {c.city}
                    </option>
                  ))}
              </select>
            </div>
          )}
        </div>
      </div>

      {/* Mandatory Disclaimer */}
      <div className="bg-amber-50/90 border border-amber-300 rounded-xl p-4 flex items-start gap-3 text-xs text-amber-950">
        <ShieldAlert className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Comparative Cutoff Advisory: </span>
          {comparisonData?.disclaimer ||
            "Cutoff comparisons represent historical KEA closing ranks. Actual seat allotment is determined by the current counseling year's competition and seat matrix."}
        </div>
      </div>

      {loading && (
        <div className="text-center py-20 bg-white rounded-2xl border border-slate-200">
          <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm font-semibold text-slate-700">Assembling side-by-side matrices...</p>
        </div>
      )}

      {error && (
        <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl text-center">
          <p className="text-sm font-bold text-rose-900">{error}</p>
        </div>
      )}

      {/* Matrix Table */}
      {!loading && !error && comparisonData && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/80">
                <th className="p-4 font-bold text-slate-500 uppercase text-[10px] w-48 sticky left-0 bg-slate-50/80">
                  Feature / College
                </th>
                {comparisonData.colleges.map((col) => (
                  <th key={col.college_id} className="p-4 font-bold text-slate-900 text-sm min-w-[240px]">
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-1.5">
                          <span className="px-2 py-0.5 bg-slate-200 text-slate-800 rounded font-extrabold text-[10px]">
                            {col.code}
                          </span>
                          <span className="text-slate-500 text-[11px]">{col.city}</span>
                        </div>
                        <span className="block font-black text-slate-900 text-base mt-1">
                          {col.short_name}
                        </span>
                        <span className="text-[11px] text-slate-500 font-normal">{col.name}</span>
                      </div>
                      <button
                        onClick={() => handleRemoveCollege(col.college_id)}
                        className="p-1 text-slate-400 hover:text-rose-600 rounded-lg"
                        title="Remove from comparison"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
              {/* Branch Under Evaluation */}
              <tr className="bg-indigo-50/40">
                <td className="p-4 font-bold text-indigo-900 uppercase text-[10px] sticky left-0 bg-indigo-50/40">
                  Branch Code & Name
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 font-bold text-indigo-950">
                    {col.branch_name} ({col.branch_code})
                  </td>
                ))}
              </tr>

              {/* Historical Closing Cutoffs */}
              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  2025 Closing Cutoff ({category})
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 font-extrabold text-sm text-brand-700">
                    {col.cutoffs_by_year[2025] ? col.cutoffs_by_year[2025].toLocaleString() : 'N/A'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  2024 Closing Cutoff ({category})
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 font-extrabold text-sm text-slate-800">
                    {col.cutoffs_by_year[2024] ? col.cutoffs_by_year[2024].toLocaleString() : 'N/A'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  2023 Closing Cutoff ({category})
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 font-extrabold text-sm text-slate-800">
                    {col.cutoffs_by_year[2023] ? col.cutoffs_by_year[2023].toLocaleString() : 'N/A'}
                  </td>
                ))}
              </tr>

              {/* Placements */}
              <tr className="bg-emerald-50/30">
                <td className="p-4 font-bold text-emerald-900 uppercase text-[10px] sticky left-0 bg-emerald-50/30">
                  Median CTC (LPA)
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 font-extrabold text-emerald-900 text-sm">
                    {col.placement?.median_package_lpa ? `₹${col.placement.median_package_lpa} LPA` : 'N/A'}
                  </td>
                ))}
              </tr>

              <tr className="bg-emerald-50/30">
                <td className="p-4 font-bold text-emerald-900 uppercase text-[10px] sticky left-0 bg-emerald-50/30">
                  Highest CTC (LPA)
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 font-extrabold text-emerald-900 text-sm">
                    {col.placement?.highest_package_lpa ? `₹${col.placement.highest_package_lpa} LPA` : 'N/A'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  Key Recruiters
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4">
                    <div className="flex flex-wrap gap-1">
                      {(col.placement?.top_recruiters || []).slice(0, 3).map((rec, i) => (
                        <span key={i} className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-[10px] font-semibold">
                          {rec}
                        </span>
                      ))}
                    </div>
                  </td>
                ))}
              </tr>

              {/* Campus & Infrastructure */}
              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  Campus Area
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4">
                    {col.campus_area_acres ? `${col.campus_area_acres} Acres` : 'N/A'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  Hostel Availability
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4">
                    {col.hostel_facility ? 'Hostels on Campus' : 'Day Scholars'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  NAAC / NBA Accreditation
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 font-semibold text-slate-900">
                    {col.accreditation || 'Recognized'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  Data Citation
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4 text-slate-500 text-[11px]">
                    {col.source}
                  </td>
                ))}
              </tr>

              {/* Action Links */}
              <tr>
                <td className="p-4 font-bold text-slate-500 uppercase text-[10px] sticky left-0 bg-white">
                  Deep Dive
                </td>
                {comparisonData.colleges.map((col) => (
                  <td key={col.college_id} className="p-4">
                    <Link
                      to={`/cet/colleges/${col.college_id}?branch=${col.branch_code}&category=${category}`}
                      className="px-3 py-1.5 bg-brand-50 hover:bg-brand-100 text-brand-700 font-bold rounded-xl text-xs inline-flex items-center gap-1 transition-colors"
                    >
                      <span>Full Trends Profile</span>
                      <ExternalLink className="w-3 h-3" />
                    </Link>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
