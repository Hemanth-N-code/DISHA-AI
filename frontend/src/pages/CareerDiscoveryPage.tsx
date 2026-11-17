// frontend/src/pages/CareerDiscoveryPage.tsx
import React, { useState, useEffect } from 'react';
import { Search, Sparkles, Filter, SlidersHorizontal, Scale, RefreshCw, Info } from 'lucide-react';
import { api } from '../services/api';
import { CareerCandidate } from '../types';
import { CareerCard } from '../components/CareerCard';
import { CDIBadge } from '../components/CDIBadge';

export const CareerDiscoveryPage: React.FC = () => {
  const [candidates, setCandidates] = useState<CareerCandidate[]>([]);
  const [cdi, setCdi] = useState<number>(0.88);
  const [domains, setDomains] = useState<string[]>([]);
  const [strategy, setStrategy] = useState<string>('Diversity-Aware Discovery');
  
  const [selectedDomain, setSelectedDomain] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [applyDiversity, setApplyDiversity] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(true);

  // Compare shortlist state
  const [compareIds, setCompareIds] = useState<string[]>([]);

  const fetchDiscovery = async () => {
    setLoading(true);
    try {
      const res = await api.careers.discover(applyDiversity, selectedDomain || undefined);
      setCandidates(res.candidates);
      setCdi(res.career_diversity_index);
      setDomains(res.domains_represented);
      setStrategy(res.discovery_strategy);
    } catch (err) {
      console.warn('Failed to load career universe:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDiscovery();
  }, [applyDiversity, selectedDomain]);

  const handleToggleSave = async (id: string, name: string) => {
    await api.memory.toggleSave(id, name);
  };

  const handleToggleCompare = (id: string) => {
    if (compareIds.includes(id)) {
      setCompareIds(compareIds.filter((cid) => cid !== id));
    } else {
      if (compareIds.length >= 4) {
        alert('You can compare up to 4 careers simultaneously.');
        return;
      }
      setCompareIds([...compareIds, id]);
    }
  };

  const filteredCandidates = candidates.filter((c) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      c.career_name.toLowerCase().includes(q) ||
      c.description.toLowerCase().includes(q) ||
      c.domain.toLowerCase().includes(q)
    );
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-brand-50 text-brand-700 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5 text-brand-600" />
            <span>Research Novelty #2: Career Diversity-Aware Discovery</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            Your Career Universe
          </h1>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl">
            Beyond conventional popularity algorithms. DISHA calculates transparent fit across 5 pillars while guaranteeing multi-domain exposure to break algorithmic echo-chambers.
          </p>
        </div>

        {/* CDI Badge & Diversity Toggle */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
          <CDIBadge score={cdi} domainsCount={domains.length} strategy={strategy} />
          
          {/* Baseline vs Diversity-Aware Switch for IEEE Demo */}
          <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm text-xs">
            <span className="font-semibold text-slate-700">Mode:</span>
            <button
              type="button"
              onClick={() => setApplyDiversity(true)}
              className={`px-2.5 py-1 rounded-md font-bold transition-all ${
                applyDiversity
                  ? 'bg-brand-600 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
              title="DISHA Diversity-Aware Algorithm"
            >
              Diversity Aware
            </button>
            <button
              type="button"
              onClick={() => setApplyDiversity(false)}
              className={`px-2.5 py-1 rounded-md font-bold transition-all ${
                !applyDiversity
                  ? 'bg-slate-800 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
              title="Standard Top-K Baseline Recommender (Prone to popularity bias)"
            >
              Baseline Top-K
            </button>
          </div>
        </div>
      </div>

      {/* Compare Floating Drawer Bar if careers selected */}
      {compareIds.length > 0 && (
        <div className="p-4 rounded-xl bg-brand-900 text-white flex items-center justify-between shadow-lg">
          <div className="flex items-center gap-2 text-xs">
            <Scale className="w-4 h-4 text-brand-300" />
            <span className="font-bold">{compareIds.length} career(s) selected for comparison</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCompareIds([])}
              className="text-xs text-slate-400 hover:text-white px-2 py-1"
            >
              Clear
            </button>
            <a
              href={`/compare?ids=${compareIds.join(',')}`}
              className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-white text-brand-900 font-bold text-xs hover:bg-slate-100"
            >
              <span>Launch Side-by-Side Comparison</span>
            </a>
          </div>
        </div>
      )}

      {/* Filter Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm space-y-3">
        <div className="flex flex-col sm:flex-row items-center gap-3">
          {/* Search */}
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search careers, domains, or competencies..."
              className="w-full pl-9 pr-3 py-2 rounded-lg border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </div>

          {/* Domain Dropdown */}
          <div className="w-full sm:w-64">
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-slate-200 text-xs font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500 bg-white"
            >
              <option value="">All 17 Domains Spanned</option>
              <option value="Engineering & Technology">Engineering & Technology</option>
              <option value="AI & Data">AI & Data</option>
              <option value="Cybersecurity">Cybersecurity</option>
              <option value="Design">Design</option>
              <option value="Fashion">Fashion</option>
              <option value="Media & Film">Media & Film</option>
              <option value="Psychology">Psychology</option>
              <option value="Fine Arts">Fine Arts</option>
              <option value="Healthcare">Healthcare</option>
              <option value="Business & Finance">Business & Finance</option>
              <option value="Law">Law</option>
              <option value="Agriculture">Agriculture</option>
              <option value="Environment">Environment</option>
              <option value="Hospitality & Tourism">Hospitality & Tourism</option>
              <option value="Education">Education</option>
              <option value="Skilled/Vocational">Skilled/Vocational</option>
              <option value="Emerging Careers">Emerging Careers</option>
            </select>
          </div>
        </div>

        {/* Explainability note */}
        <div className="flex items-center gap-2 text-[11px] text-slate-500 pt-2 border-t border-slate-100">
          <Info className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <span>
            {applyDiversity
              ? 'Multi-objective re-ranking is active. Surfacing high-affinity candidates across engineering, design, and adjacent verticals.'
              : 'Baseline top-k ranking active. Demonstrates popularity clustering where tech candidates dominate results.'}
          </span>
        </div>
      </div>

      {/* Career Grid */}
      {loading ? (
        <div className="py-16 flex flex-col items-center justify-center gap-3">
          <div className="w-8 h-8 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin" />
          <p className="text-xs text-slate-500">Retrieving candidate careers across universe...</p>
        </div>
      ) : filteredCandidates.length === 0 ? (
        <div className="py-16 bg-white rounded-xl border border-slate-200 text-center p-8">
          <p className="text-sm font-bold text-slate-700">No careers found matching filter criteria.</p>
          <p className="text-xs text-slate-500 mt-1">Try resetting the domain filter or search keyword.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredCandidates.map((cand) => (
            <CareerCard
              key={cand.career_id}
              candidate={cand}
              onToggleSave={handleToggleSave}
              onAddToCompare={handleToggleCompare}
              isCompared={compareIds.includes(cand.career_id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};
