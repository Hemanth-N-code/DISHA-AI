// frontend/src/pages/CareerGraphPage.tsx
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  MarkerType,
  Handle,
  Position,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { GitFork, ArrowLeft, Sliders, MapPin, Compass, Sparkles, Layers, ArrowUpRight, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';
import { CareerDetail } from '../types';

// Custom Node Component for React Flow
const CareerNodeCustom: React.FC<{ data: any }> = ({ data }) => {
  const isCenter = data.isCenter;

  return (
    <div
      className={`px-4 py-3 rounded-xl border shadow-md transition-all cursor-pointer min-w-[200px] max-w-[260px] ${
        isCenter
          ? 'bg-gradient-to-br from-brand-900 to-indigo-950 border-brand-500 text-white shadow-brand-500/20 ring-2 ring-brand-400'
          : 'bg-white border-slate-200 hover:border-brand-300 text-slate-800 hover:shadow-lg'
      }`}
    >
      <Handle type="target" position={Position.Top} className="!bg-brand-500" />
      <div className="flex items-center justify-between mb-1.5">
        <span
          className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider ${
            isCenter
              ? 'bg-brand-600/80 text-brand-100'
              : 'bg-indigo-50 text-indigo-700 border border-indigo-100'
          }`}
        >
          {data.domain || 'Domain'}
        </span>
        {isCenter && (
          <span className="flex items-center text-[10px] text-amber-300 font-medium gap-0.5">
            <Sparkles className="w-3 h-3" /> Focal
          </span>
        )}
      </div>

      <div className={`font-bold text-sm leading-snug mb-1 ${isCenter ? 'text-white' : 'text-slate-900'}`}>
        {data.label}
      </div>

      {data.relationType && (
        <div className="text-[11px] font-medium text-brand-600 mb-1">
          {data.relationType}
        </div>
      )}

      <p className={`text-[11px] line-clamp-2 ${isCenter ? 'text-brand-200' : 'text-slate-500'}`}>
        {data.description}
      </p>
      <Handle type="source" position={Position.Bottom} className="!bg-brand-500" />
    </div>
  );
};

const nodeTypes = {
  careerNode: CareerNodeCustom,
};

export const CareerGraphPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const currentCareerId = id || 'ux_designer';

  const [careerList, setCareerList] = useState<CareerDetail[]>([]);
  const [selectedNodeData, setSelectedNodeData] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Load career catalog for switching root career
  useEffect(() => {
    api.careers.list().then((list) => setCareerList(list)).catch(console.warn);
  }, []);

  // Fetch graph data whenever currentCareerId changes
  useEffect(() => {
    setLoading(true);
    api.careers.getGraph(currentCareerId)
      .then((res) => {
        // Format nodes
        const formattedNodes: Node[] = res.nodes.map((n: any) => ({
          id: n.id,
          type: 'careerNode',
          data: n.data,
          position: n.position || { x: 300, y: 300 },
        }));

        // Format edges with styling
        const formattedEdges: Edge[] = res.edges.map((e: any) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          label: e.label,
          animated: e.animated || false,
          style: e.style || { stroke: '#6366f1', strokeWidth: 2 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: e.style?.stroke || '#6366f1',
          },
          labelStyle: { fill: '#475569', fontSize: 11, fontWeight: 500 },
          labelBgStyle: { fill: '#ffffff', rx: 4, ry: 4 },
        }));

        setNodes(formattedNodes);
        setEdges(formattedEdges);

        // Default selection to center node
        const centerNode = formattedNodes.find((n) => n.data.isCenter);
        if (centerNode) {
          setSelectedNodeData(centerNode.data);
        }
      })
      .catch((err) => {
        console.error('Failed to load career graph:', err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [currentCareerId, setNodes, setEdges]);

  const onNodeClick = useCallback((_: any, node: Node) => {
    setSelectedNodeData(node.data);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Top Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Link
              to={`/careers/${currentCareerId}`}
              className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                  <GitFork className="w-5 h-5 text-brand-600" />
                  Alternative Career Path Graph
                </h1>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-brand-50 text-brand-700 font-semibold border border-brand-200">
                  Novelty #3: Decision Space
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Explore connected pivots, lateral bridges, and adjacent specializations instead of dead-end recommendations.
              </p>
            </div>
          </div>

          {/* Focal Career Switcher */}
          <div className="flex items-center gap-2">
            <label className="text-xs font-medium text-slate-600">Focal Career:</label>
            <select
              value={currentCareerId}
              onChange={(e) => navigate(`/graph/${e.target.value}`)}
              className="text-xs bg-slate-50 border border-slate-300 rounded-lg px-3 py-2 text-slate-800 focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
            >
              {careerList.map((c) => (
                <option key={c.career_id} value={c.career_id}>
                  {c.career_name} ({c.domain})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Graph Content & Side Inspector */}
      <div className="flex-1 flex flex-col lg:flex-row relative">
        {/* Interactive React Flow Canvas */}
        <div className="flex-1 h-[650px] lg:h-auto bg-slate-950/5 relative">
          {loading ? (
            <div className="absolute inset-0 flex items-center justify-center bg-white/70 z-10">
              <div className="text-center">
                <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
                <p className="text-sm font-medium text-slate-700">Synthesizing Career Pivot Topology...</p>
              </div>
            </div>
          ) : null}

          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <Background color="#cbd5e1" gap={20} size={1} />
            <Controls className="!bg-white !border-slate-200 !shadow-sm !rounded-lg" />
            <MiniMap
              nodeColor={(n: any) => (n.data?.isCenter ? '#4338ca' : '#94a3b8')}
              className="!bg-white !border !border-slate-200 !rounded-lg !shadow-sm"
            />
          </ReactFlow>

          {/* Graph Legend Overlay */}
          <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm border border-slate-200 rounded-xl p-3 shadow-sm text-xs space-y-2 pointer-events-none">
            <div className="font-semibold text-slate-800 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-brand-600" /> Graph Structure
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-indigo-900 ring-2 ring-brand-400" />
              <span className="text-slate-600 font-medium">Focal Target Career</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-4 h-0.5 bg-brand-600" />
              <span className="text-slate-600">Alternative Lateral Pivot</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-4 h-0.5 border-t-2 border-dashed border-cyan-500" />
              <span className="text-slate-600">Adjacent Specialization</span>
            </div>
          </div>
        </div>

        {/* Right Inspector Drawer */}
        <div className="w-full lg:w-96 bg-white border-t lg:border-t-0 lg:border-l border-slate-200 p-6 flex flex-col justify-between overflow-y-auto">
          {selectedNodeData ? (
            <div className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-brand-50 text-brand-700 border border-brand-100 uppercase tracking-wider">
                    {selectedNodeData.domain}
                  </span>
                  {selectedNodeData.isCenter && (
                    <span className="text-xs bg-amber-100 text-amber-800 font-medium px-2 py-0.5 rounded-full flex items-center gap-1">
                      <Sparkles className="w-3 h-3" /> Current Focus
                    </span>
                  )}
                </div>
                <h2 className="text-xl font-bold text-slate-900 mb-1">
                  {selectedNodeData.label}
                </h2>
                {selectedNodeData.relationType && (
                  <p className="text-xs font-semibold text-brand-600 mb-3">
                    Relationship: {selectedNodeData.relationType}
                  </p>
                )}
                <p className="text-sm text-slate-600 leading-relaxed">
                  {selectedNodeData.description}
                </p>
              </div>

              {/* Research Insight Callout */}
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs space-y-2">
                <div className="font-semibold text-slate-800 flex items-center gap-1.5">
                  <Compass className="w-4 h-4 text-brand-600" /> Why Alternative Graphs Matter
                </div>
                <p className="text-slate-600 leading-relaxed">
                  In traditional counseling, choosing an option closes off other paths. In DISHA's decision space, this career shares 60%+ skill overlap with neighboring nodes, meaning your learning milestones keep future pivots wide open.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="space-y-2.5 pt-2">
                <Link
                  to={`/careers/${selectedNodeData.careerId || selectedNodeData.id}`}
                  className="w-full inline-flex items-center justify-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-medium py-2.5 px-4 rounded-xl text-sm transition-colors shadow-sm"
                >
                  View Career Deep Dive
                  <ArrowUpRight className="w-4 h-4" />
                </Link>

                <button
                  onClick={() => navigate(`/graph/${selectedNodeData.careerId || selectedNodeData.id}`)}
                  className="w-full inline-flex items-center justify-center gap-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-medium py-2.5 px-4 rounded-xl text-sm transition-colors"
                >
                  Re-Center Graph on This Career
                </button>

                <Link
                  to={`/skill-gap/${selectedNodeData.careerId || selectedNodeData.id}`}
                  className="w-full inline-flex items-center justify-center gap-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-medium py-2.5 px-4 rounded-xl text-sm transition-colors"
                >
                  Analyze Skill Gap
                </Link>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-slate-500">
              <Compass className="w-10 h-10 text-slate-400 mx-auto mb-2 animate-pulse" />
              <p className="text-sm font-medium">Click any node on the graph to inspect its details and pivot bridges.</p>
            </div>
          )}

          <div className="pt-6 border-t border-slate-100 mt-6 text-[11px] text-slate-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
            Graph automatically updates dynamically based on O*NET and ESCO skill adjacency mappings.
          </div>
        </div>
      </div>
    </div>
  );
};
