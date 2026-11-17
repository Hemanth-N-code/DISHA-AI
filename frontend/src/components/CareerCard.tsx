// frontend/src/components/CareerCard.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Bookmark, Compass, Scale, Sparkles } from 'lucide-react';
import { CareerCandidate } from '../types';
import { FactorTagBadge } from './FactorTagBadge';

interface CareerCardProps {
  candidate: CareerCandidate;
  isSaved?: boolean;
  onToggleSave?: (id: string, name: string) => void;
  onAddToCompare?: (id: string) => void;
  isCompared?: boolean;
}

export const CareerCard: React.FC<CareerCardProps> = ({
  candidate,
  isSaved,
  onToggleSave,
  onAddToCompare,
  isCompared
}) => {
  const { score_breakdown } = candidate;
  const score = score_breakdown.overall_score;

  // Domain badge color map
  const getDomainStyle = (domain: string) => {
    switch (domain) {
      case 'Engineering & Technology': return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'AI & Data': return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'Cybersecurity': return 'bg-red-50 text-red-700 border-red-200';
      case 'Design': return 'bg-pink-50 text-pink-700 border-pink-200';
      case 'Fine Arts': return 'bg-orange-50 text-orange-700 border-orange-200';
      case 'Healthcare': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Business & Finance': return 'bg-amber-50 text-amber-800 border-amber-200';
      case 'Law': return 'bg-stone-50 text-stone-700 border-stone-200';
      case 'Environment': return 'bg-teal-50 text-teal-700 border-teal-200';
      case 'Emerging Careers': return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      default: return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="flex flex-col justify-between bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md hover:border-brand-300 transition-all duration-200">
      <div>
        {/* Header: Domain & Save */}
        <div className="flex items-center justify-between gap-2 mb-2">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className={`text-[11px] font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${getDomainStyle(candidate.domain)}`}>
              {candidate.domain}
            </span>
            {candidate.is_diversity_highlight && (
              <span className="inline-flex items-center gap-1 text-[11px] font-semibold bg-amber-50 text-amber-800 border border-amber-200 px-2 py-0.5 rounded-full">
                <Sparkles className="w-2.5 h-2.5 text-amber-600" />
                Diversity Surface
              </span>
            )}
          </div>
          {onToggleSave && (
            <button
              onClick={() => onToggleSave(candidate.career_id, candidate.career_name)}
              className={`p-1.5 rounded-lg transition-colors ${
                isSaved ? 'text-amber-500 bg-amber-50' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-50'
              }`}
              title={isSaved ? 'Saved in Career Memory' : 'Save to short-term bookmarks'}
            >
              <Bookmark className="w-4 h-4" fill={isSaved ? 'currentColor' : 'none'} />
            </button>
          )}
        </div>

        {/* Title */}
        <h3 className="text-lg font-bold text-slate-900 mb-1 leading-snug">
          <Link to={`/careers/${candidate.career_id}`} className="hover:text-brand-600 transition-colors">
            {candidate.career_name}
          </Link>
        </h3>

        {/* Description snippet */}
        <p className="text-xs text-slate-600 line-clamp-2 mb-4 leading-relaxed">
          {candidate.description}
        </p>

        {/* Compatibility Bar */}
        <div className="mb-4">
          <div className="flex items-center justify-between text-xs mb-1">
            <span className="font-medium text-slate-700">Exploratory Compatibility</span>
            <span className="font-bold text-brand-700">{score}%</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                score >= 80 ? 'bg-gradient-to-r from-emerald-500 to-teal-500' :
                score >= 65 ? 'bg-gradient-to-r from-brand-500 to-indigo-600' :
                'bg-gradient-to-r from-amber-500 to-orange-500'
              }`}
              style={{ width: `${Math.min(100, Math.max(10, score))}%` }}
            />
          </div>
        </div>

        {/* Factor Tags (Transparent explainability) */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {score_breakdown.factor_tags.slice(0, 3).map((tag, idx) => (
            <FactorTagBadge key={idx} tag={tag} />
          ))}
        </div>
      </div>

      {/* Action Footer */}
      <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5">
          {onAddToCompare && (
            <button
              onClick={() => onAddToCompare(candidate.career_id)}
              className={`inline-flex items-center gap-1 text-xs font-medium px-2.5 py-1.5 rounded-lg border transition-colors ${
                isCompared
                  ? 'bg-brand-50 text-brand-700 border-brand-300'
                  : 'text-slate-600 bg-white border-slate-200 hover:bg-slate-50'
              }`}
            >
              <Scale className="w-3.5 h-3.5" />
              <span>{isCompared ? 'Comparing' : 'Compare'}</span>
            </button>
          )}
          <Link
            to={`/graph?center=${candidate.career_id}`}
            className="p-1.5 text-slate-500 hover:text-brand-600 hover:bg-brand-50 rounded-lg border border-slate-200"
            title="Explore Alternative Path Graph"
          >
            <Compass className="w-4 h-4" />
          </Link>
        </div>

        <Link
          to={`/careers/${candidate.career_id}`}
          className="inline-flex items-center gap-1 text-xs font-semibold text-brand-600 hover:text-brand-700 hover:underline"
        >
          <span>Explore Path</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
