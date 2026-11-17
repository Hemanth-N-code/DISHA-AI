// frontend/src/pages/RoadmapPage.tsx
import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import {
  Milestone, CheckCircle2, Circle, Clock, Sparkles, Download,
  ExternalLink, Layers, ArrowLeft, RefreshCw, FolderGit2, Check,
  ChevronRight, ArrowRight
} from 'lucide-react';
import { api } from '../services/api';
import { Roadmap, RoadmapTask, CareerDetail } from '../types';

export const RoadmapPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const careerId = searchParams.get('career') || 'ux_designer';

  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [careerList, setCareerList] = useState<CareerDetail[]>([]);
  const [horizonMonths, setHorizonMonths] = useState<number>(6);
  const [loading, setLoading] = useState<boolean>(true);
  const [editingArtifactTaskId, setEditingArtifactTaskId] = useState<number | null>(null);
  const [artifactInput, setArtifactInput] = useState<string>('');
  const [copied, setCopied] = useState<boolean>(false);

  useEffect(() => {
    api.careers.list().then(setCareerList).catch(console.warn);
  }, []);

  const loadRoadmap = async () => {
    setLoading(true);
    try {
      // First try to get active roadmap; if not found, generate one
      let data = await api.roadmap.getActive(careerId).catch(() => null);
      if (!data) {
        data = await api.roadmap.generate(careerId, horizonMonths);
      }
      setRoadmap(data);
    } catch (err) {
      console.error('Failed to load roadmap:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRoadmap();
  }, [careerId, horizonMonths]);

  const handleToggleTaskStatus = async (task: RoadmapTask) => {
    if (!roadmap) return;
    const nextStatus =
      task.status === 'not_started'
        ? 'in_progress'
        : task.status === 'in_progress'
        ? 'completed'
        : 'not_started';

    try {
      const updated = await api.roadmap.updateTask(task.id, nextStatus);
      // Update local state
      const updatedTasks = roadmap.tasks.map((t) => (t.id === task.id ? updated : t));
      const completedCount = updatedTasks.filter((t) => t.status === 'completed').length;
      const progress = Math.round((completedCount / updatedTasks.length) * 100);

      setRoadmap({
        ...roadmap,
        tasks: updatedTasks,
        overall_progress: progress,
      });
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleSaveArtifact = async (taskId: number) => {
    if (!roadmap) return;
    try {
      const updated = await api.roadmap.updateTask(taskId, undefined, artifactInput);
      setRoadmap({
        ...roadmap,
        tasks: roadmap.tasks.map((t) => (t.id === taskId ? updated : t)),
      });
      setEditingArtifactTaskId(null);
      setArtifactInput('');
    } catch (err) {
      console.error('Failed to update artifact:', err);
    }
  };

  const handleExportMarkdown = () => {
    if (!roadmap) return;
    let md = `# Actionable Milestone Roadmap: ${roadmap.career_name}\n`;
    md += `**Target Horizon:** ${roadmap.target_horizon_months} Months\n`;
    md += `**Overall Progress:** ${roadmap.overall_progress}%\n\n`;

    const stageNames = [
      'Foundations & Core Prerequisites',
      'Applied Skills & Mini Projects',
      'Real-World Portfolio & Practical Artifacts',
      'Entry Applications & Capstone',
    ];

    for (let s = 1; s <= 4; s++) {
      const tasks = roadmap.tasks.filter((t) => t.stage_index === s);
      if (tasks.length === 0) continue;
      md += `## Stage ${s}: ${stageNames[s - 1]}\n`;
      tasks.forEach((t) => {
        const check = t.status === 'completed' ? '[x]' : '[ ]';
        md += `- ${check} **${t.title}** (${t.estimated_weeks} weeks) - ${t.description}\n`;
        if (t.portfolio_artifact) {
          md += `  - Artifact: ${t.portfolio_artifact}\n`;
        }
      });
      md += '\n';
    }

    navigator.clipboard.writeText(md);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const stageNames = [
    'Stage 1: Foundations & Core Prerequisites',
    'Stage 2: Applied Skills & Mini Projects',
    'Stage 3: Real-World Portfolio & Practical Artifacts',
    'Stage 4: Entry Applications & Capstone Verification',
  ];

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Top Header */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Link
                  to={`/careers/${careerId}`}
                  className="p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  <ArrowLeft className="w-4 h-4" />
                </Link>
                <span className="text-xs px-3 py-1 rounded-full bg-brand-50 text-brand-700 font-semibold border border-brand-200 uppercase tracking-wider">
                  Novelty #6: Actionable Milestone DAG
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2.5">
                <Milestone className="w-7 h-7 text-brand-600" />
                Personalized Career Roadmap
              </h1>
              <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-2xl">
                A non-generic sequence of stages, actionable projects, and verifiable artifacts customized to your skill gaps.
              </p>
            </div>

            {/* Target Career & Horizon Controls */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
              <div>
                <label className="block text-[11px] font-semibold text-slate-500 mb-1 uppercase">
                  Target Career
                </label>
                <select
                  value={careerId}
                  onChange={(e) => {
                    setSearchParams({ career: e.target.value });
                  }}
                  className="text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
                >
                  {careerList.map((c) => (
                    <option key={c.career_id} value={c.career_id}>
                      {c.career_name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-500 mb-1 uppercase">
                  Time Horizon
                </label>
                <select
                  value={horizonMonths}
                  onChange={(e) => setHorizonMonths(Number(e.target.value))}
                  className="text-xs bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
                >
                  <option value={3}>3 Months (Accelerated)</option>
                  <option value={6}>6 Months (Balanced)</option>
                  <option value={12}>12 Months (Comprehensive)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Progress & Quick Actions Bar */}
        {roadmap && (
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex-1 w-full md:w-auto">
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <span>Execution Progress:</span>
                  <span className="text-brand-600">{roadmap.overall_progress}% Complete</span>
                </div>
                <span className="text-xs text-slate-500 font-medium">
                  {roadmap.tasks.filter((t) => t.status === 'completed').length} of {roadmap.tasks.length} Milestones Finished
                </span>
              </div>
              <div className="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
                <div
                  className="bg-brand-600 h-full rounded-full transition-all duration-500"
                  style={{ width: `${roadmap.overall_progress}%` }}
                />
              </div>
            </div>

            <div className="flex items-center gap-2 self-end md:self-auto">
              <button
                type="button"
                onClick={handleExportMarkdown}
                className="inline-flex items-center gap-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold px-4 py-2.5 rounded-xl transition-colors"
              >
                {copied ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-600" /> Copied Markdown!
                  </>
                ) : (
                  <>
                    <Download className="w-3.5 h-3.5" /> Export Markdown
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={loadRoadmap}
                className="p-2.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-xl transition-colors"
                title="Regenerate Roadmap"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Stages & Tasks */}
        {loading ? (
          <div className="bg-white border border-slate-200 rounded-2xl p-16 text-center shadow-sm">
            <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-sm font-medium text-slate-700">Synthesizing personalized milestone DAG...</p>
          </div>
        ) : roadmap ? (
          <div className="space-y-8">
            {[1, 2, 3, 4].map((stageIndex) => {
              const stageTasks = roadmap.tasks.filter((t) => t.stage_index === stageIndex);
              if (stageTasks.length === 0) return null;

              const stageCompleted = stageTasks.filter((t) => t.status === 'completed').length;

              return (
                <div key={stageIndex} className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
                  {/* Stage Header */}
                  <div className="bg-slate-50/70 border-b border-slate-200 px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-xl bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-sm">
                        {stageIndex}
                      </div>
                      <div>
                        <h2 className="font-bold text-base text-slate-900">
                          {stageNames[stageIndex - 1]}
                        </h2>
                        <span className="text-xs text-slate-500">
                          {stageCompleted} of {stageTasks.length} tasks completed
                        </span>
                      </div>
                    </div>

                    <div className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-200/70 text-slate-700">
                      ~{stageTasks.reduce((acc, t) => acc + t.estimated_weeks, 0)} Weeks
                    </div>
                  </div>

                  {/* Tasks List */}
                  <div className="divide-y divide-slate-100">
                    {stageTasks.map((task) => {
                      const isCompleted = task.status === 'completed';
                      const isInProgress = task.status === 'in_progress';

                      return (
                        <div
                          key={task.id}
                          className={`p-6 transition-colors ${
                            isCompleted
                              ? 'bg-emerald-50/30'
                              : isInProgress
                              ? 'bg-indigo-50/20'
                              : 'hover:bg-slate-50/60'
                          }`}
                        >
                          <div className="flex items-start gap-4">
                            {/* Checkbox Status Trigger */}
                            <button
                              type="button"
                              onClick={() => handleToggleTaskStatus(task)}
                              className="mt-1 focus:outline-none"
                              title="Click to advance status (Not Started → In Progress → Completed)"
                            >
                              {isCompleted ? (
                                <CheckCircle2 className="w-6 h-6 text-emerald-600 fill-emerald-100" />
                              ) : isInProgress ? (
                                <div className="w-6 h-6 rounded-full border-2 border-brand-500 flex items-center justify-center">
                                  <div className="w-2.5 h-2.5 bg-brand-600 rounded-full animate-pulse" />
                                </div>
                              ) : (
                                <Circle className="w-6 h-6 text-slate-300 hover:text-slate-500 transition-colors" />
                              )}
                            </button>

                            {/* Task Content */}
                            <div className="flex-1 space-y-2">
                              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                                <h3
                                  className={`text-base font-bold ${
                                    isCompleted ? 'text-slate-500 line-through' : 'text-slate-900'
                                  }`}
                                >
                                  {task.title}
                                </h3>

                                <div className="flex items-center gap-2">
                                  <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-600 uppercase tracking-wider">
                                    {task.category}
                                  </span>
                                  <span className="text-xs text-slate-500 flex items-center gap-1">
                                    <Clock className="w-3.5 h-3.5" /> {task.estimated_weeks} wks
                                  </span>
                                </div>
                              </div>

                              <p className="text-sm text-slate-600 leading-relaxed">
                                {task.description}
                              </p>

                              {/* Artifact section */}
                              <div className="pt-2 flex flex-col sm:flex-row sm:items-center gap-2">
                                {editingArtifactTaskId === task.id ? (
                                  <div className="flex items-center gap-2 w-full max-w-md">
                                    <input
                                      type="text"
                                      placeholder="https://github.com/your-username/project..."
                                      value={artifactInput}
                                      onChange={(e) => setArtifactInput(e.target.value)}
                                      className="flex-1 text-xs px-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
                                    />
                                    <button
                                      type="button"
                                      onClick={() => handleSaveArtifact(task.id)}
                                      className="text-xs bg-brand-600 text-white font-semibold px-3 py-1.5 rounded-lg hover:bg-brand-700"
                                    >
                                      Save
                                    </button>
                                    <button
                                      type="button"
                                      onClick={() => setEditingArtifactTaskId(null)}
                                      className="text-xs text-slate-500 hover:text-slate-800"
                                    >
                                      Cancel
                                    </button>
                                  </div>
                                ) : task.portfolio_artifact ? (
                                  <div className="inline-flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-lg text-xs text-slate-700 font-medium">
                                    <FolderGit2 className="w-3.5 h-3.5 text-brand-600" />
                                    <span>Artifact:</span>
                                    <a
                                      href={task.portfolio_artifact}
                                      target="_blank"
                                      rel="noreferrer"
                                      className="text-brand-600 underline font-semibold flex items-center gap-1"
                                    >
                                      {task.portfolio_artifact}
                                      <ExternalLink className="w-3 h-3" />
                                    </a>
                                    <button
                                      type="button"
                                      onClick={() => {
                                        setEditingArtifactTaskId(task.id);
                                        setArtifactInput(task.portfolio_artifact || '');
                                      }}
                                      className="text-slate-400 hover:text-slate-700 text-[10px] ml-1"
                                    >
                                      Edit
                                    </button>
                                  </div>
                                ) : (
                                  <button
                                    type="button"
                                    onClick={() => {
                                      setEditingArtifactTaskId(task.id);
                                      setArtifactInput('');
                                    }}
                                    className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1"
                                  >
                                    <FolderGit2 className="w-3.5 h-3.5" /> + Attach Portfolio Link / Artifact
                                  </button>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        ) : null}
      </div>
    </div>
  );
};
