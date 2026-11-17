// frontend/src/components/FactorTagBadge.tsx
import React from 'react';
import { CheckCircle2, AlertCircle } from 'lucide-react';
import { FactorTag } from '../types';

export const FactorTagBadge: React.FC<{ tag: FactorTag }> = ({ tag }) => {
  if (tag.positive) {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-200">
        <CheckCircle2 className="w-3 h-3 text-emerald-600 shrink-0" />
        <span>{tag.text}</span>
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-900 border border-amber-200">
      <AlertCircle className="w-3 h-3 text-amber-600 shrink-0" />
      <span>{tag.text}</span>
    </span>
  );
};
