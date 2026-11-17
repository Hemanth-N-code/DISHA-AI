// frontend/src/components/CDIBadge.tsx
import React from 'react';
import { Sparkles } from 'lucide-react';

interface CDIBadgeProps {
  score: number;
  domainsCount?: number;
  strategy?: string;
}

export const CDIBadge: React.FC<CDIBadgeProps> = ({ score, domainsCount, strategy }) => {
  return (
    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-gradient-to-r from-brand-50 to-indigo-50 border border-brand-200 text-brand-900 shadow-sm">
      <div className="flex items-center justify-center w-6 h-6 rounded-full bg-brand-600 text-white font-bold text-xs">
        <Sparkles className="w-3.5 h-3.5" />
      </div>
      <div>
        <div className="flex items-center gap-1.5 text-xs font-semibold">
          <span>Career Diversity Index (CDI):</span>
          <span className="text-brand-700 text-sm font-bold">{score.toFixed(3)}</span>
        </div>
        {domainsCount !== undefined && (
          <p className="text-[10px] text-slate-500">
            {domainsCount} distinct domains spanned &middot; {strategy || 'Multi-Objective Re-ranking'}
          </p>
        )}
      </div>
    </div>
  );
};
