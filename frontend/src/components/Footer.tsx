// frontend/src/components/Footer.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Compass, BookOpen, GitBranch, Cpu, ShieldCheck } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 border-t border-slate-800 text-xs mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Col 1 */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-brand-500 text-white flex items-center justify-center font-bold text-sm">
                D
              </div>
              <span className="font-extrabold text-white text-base">DISHA AI</span>
            </div>
            <p className="text-slate-400 leading-relaxed">
              "Discover Your Direction. Shape Your Future."
              An Agentic AI Framework for Career Decision Exploration and Personalized Guidance.
            </p>
            <div className="flex items-center gap-2 text-[11px] text-slate-500">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>IEEE Research Architecture Spec Compliant</span>
            </div>
          </div>

          {/* Col 2 */}
          <div>
            <h4 className="font-semibold text-white mb-3 uppercase tracking-wider text-[11px]">Exploration Tools</h4>
            <ul className="space-y-2">
              <li><Link to="/discover" className="hover:text-white transition-colors">Career Universe (CDI Aware)</Link></li>
              <li><Link to="/what-if" className="hover:text-white transition-colors">What-If Counterfactual Lab</Link></li>
              <li><Link to="/graph" className="hover:text-white transition-colors">Alternative Pathway Graph</Link></li>
              <li><Link to="/compare" className="hover:text-white transition-colors">Multi-Career Comparison</Link></li>
            </ul>
          </div>

          {/* Col 3 */}
          <div>
            <h4 className="font-semibold text-white mb-3 uppercase tracking-wider text-[11px]">Decision & Action</h4>
            <ul className="space-y-2">
              <li><Link to="/roadmap" className="hover:text-white transition-colors">Personalized Milestone DAG</Link></li>
              <li><Link to="/journey" className="hover:text-white transition-colors">Longitudinal Decision Memory</Link></li>
              <li><Link to="/assistant" className="hover:text-white transition-colors">RAG Grounded Counselor</Link></li>
              <li><Link to="/research" className="hover:text-white transition-colors">IEEE Research Metrics Dashboard</Link></li>
            </ul>
          </div>

          {/* Col 4 */}
          <div>
            <h4 className="font-semibold text-white mb-3 uppercase tracking-wider text-[11px]">Core Philosophy</h4>
            <p className="text-slate-400 mb-3 leading-relaxed">
              Moves beyond one-shot career recommendation by modeling career discovery as an iterative process of exploring alternatives, evaluating counterfactuals, and bridging skill gaps.
            </p>
            <div className="p-2.5 rounded bg-slate-800/60 border border-slate-700/60 text-[11px] text-slate-400">
              <span className="font-semibold text-indigo-400">DISCOVER</span> &rarr;{' '}
              <span className="font-semibold text-cyan-400">EXPLORE</span> &rarr;{' '}
              <span className="font-semibold text-amber-400">COMPARE</span> &rarr;{' '}
              <span className="font-semibold text-emerald-400">PLAN</span>
            </div>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-slate-500 gap-2">
          <p>&copy; 2026 DISHA AI Framework. Built for academic research & student empowerment.</p>
          <p className="flex items-center gap-2">
            <Cpu className="w-3.5 h-3.5 text-brand-400" />
            <span>Deterministic Scoring &middot; LangGraph Agents &middot; pgvector RAG</span>
          </p>
        </div>
      </div>
    </footer>
  );
};
