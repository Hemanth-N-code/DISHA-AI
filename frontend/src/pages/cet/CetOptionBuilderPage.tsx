// frontend/src/pages/cet/CetOptionBuilderPage.tsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ListTodo, ArrowUp, ArrowDown, Trash2, Printer, Download,
  Save, Sparkles, ShieldAlert, CheckCircle2, AlertCircle,
  Plus, Building2, MapPin, Info, Copy
} from 'lucide-react';
import { api } from '../../services/api';
import { OptionListResponse, OptionItem } from '../../types';

export const CetOptionBuilderPage: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [listData, setListData] = useState<OptionListResponse | null>(null);
  const [items, setItems] = useState<OptionItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  const fetchOptionList = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.cet.getOptionList();
      setListData(res);
      setItems(res.items || []);
    } catch (err: any) {
      setError(err.message || 'Please log in to view or manage your personal Option Entry List.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOptionList();
  }, []);

  const moveUp = (index: number) => {
    if (index <= 0) return;
    const newItems = [...items];
    const temp = newItems[index - 1];
    newItems[index - 1] = newItems[index];
    newItems[index] = temp;
    // Update priority orders
    newItems.forEach((item, idx) => {
      item.priority_order = idx + 1;
    });
    setItems(newItems);
  };

  const moveDown = (index: number) => {
    if (index >= items.length - 1) return;
    const newItems = [...items];
    const temp = newItems[index + 1];
    newItems[index + 1] = newItems[index];
    newItems[index] = temp;
    // Update priority orders
    newItems.forEach((item, idx) => {
      item.priority_order = idx + 1;
    });
    setItems(newItems);
  };

  const handleRemove = async (itemId: number) => {
    try {
      await api.cet.removeOptionItem(itemId);
      const remaining = items.filter((it) => it.id !== itemId);
      remaining.forEach((it, idx) => {
        it.priority_order = idx + 1;
      });
      setItems(remaining);
      showToast('Option removed from list.');
    } catch (err: any) {
      showToast(err.message || 'Failed to remove option.');
    }
  };

  const handleSaveOrder = async () => {
    setSaving(true);
    try {
      const orderedIds = items.map((it) => it.id);
      const updated = await api.cet.reorderOptionList(orderedIds);
      if (updated && updated.items) {
        setListData(updated);
        setItems(updated.items);
      }
      showToast('Option priorities saved successfully!');
    } catch (err: any) {
      showToast(err.message || 'Failed to save priority order.');
    } finally {
      setSaving(false);
    }
  };

  const handleCopyToClipboard = () => {
    if (items.length === 0) return;
    const lines = [
      '# DISHA AI - KCET Option Entry Priority Sheet',
      `# Total Options: ${items.length}`,
      '------------------------------------------------------------',
      'Priority | College Code | College Name | Branch Code | Branch Name',
      '------------------------------------------------------------',
      ...items.map(
        (it) =>
          `${String(it.priority_order).padStart(2, '0')} | ${it.college_short_name.padEnd(8)} | ${it.college_name} | ${it.branch_code} | ${it.branch_name}`
      ),
      '------------------------------------------------------------',
      'Note: This is an indicative preference sheet created with DISHA AI.',
    ];
    navigator.clipboard.writeText(lines.join('\n'));
    showToast('Copied formatted Option Entry list to clipboard!');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Toast */}
      {toastMessage && (
        <div className="fixed top-20 right-6 z-50 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-xl text-xs font-semibold flex items-center gap-2 border border-slate-700 animate-fade-in print:hidden">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6 print:border-none">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-brand-700 uppercase tracking-wider mb-1">
            <ListTodo className="w-4 h-4" />
            <span>KEA Option Entry Builder</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            My Option Entry List
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Organize your preferred college & branch choices into your final priority order.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-2 print:hidden">
          <button
            onClick={handleSaveOrder}
            disabled={saving || items.length === 0}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-700 disabled:bg-slate-300 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all"
          >
            <Save className="w-3.5 h-3.5" />
            <span>{saving ? 'Saving...' : 'Save Order'}</span>
          </button>

          <button
            onClick={handleCopyToClipboard}
            disabled={items.length === 0}
            className="px-3.5 py-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors"
          >
            <Copy className="w-3.5 h-3.5" />
            <span>Copy Text</span>
          </button>

          <button
            onClick={handlePrint}
            disabled={items.length === 0}
            className="px-3.5 py-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print Sheet</span>
          </button>

          <Link
            to="/cet/explore"
            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add More Options</span>
          </Link>
        </div>
      </div>

      {/* Mandatory Disclaimer */}
      <div className="bg-amber-50/90 border border-amber-300 rounded-xl p-4 flex items-start gap-3 text-xs text-amber-950">
        <ShieldAlert className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Official Option Entry Guidance: </span>
          {listData?.disclaimer ||
            "Historical cutoffs are indicative only. KEA counselling assigns the highest eligible option in your order. You can enter as many options as you like with zero penalty."}
        </div>
      </div>

      {/* KEA Strategy Advisory Card */}
      <div className="bg-indigo-50/80 border border-indigo-200 rounded-2xl p-5 space-y-2 text-xs text-indigo-950 print:hidden">
        <div className="flex items-center gap-2 font-bold text-indigo-900 text-sm">
          <Info className="w-4 h-4 text-indigo-600" />
          <span>Strategic Option Hierarchy Tip</span>
        </div>
        <p className="leading-relaxed text-indigo-900/90">
          In KEA option entry, there is <strong>no penalty for entering ambitious colleges first</strong>. If your rank does not match your #1 option, the algorithm tests #2, then #3, and so on. Therefore, always order your options from most desired to safety cushion:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
          <div className="p-2.5 bg-white rounded-xl border border-indigo-100">
            <span className="font-extrabold text-amber-700 block">1. Ambitious Options</span>
            <span className="text-[11px] text-slate-500">Dream institutions even if historical cutoff is tighter than your rank.</span>
          </div>
          <div className="p-2.5 bg-white rounded-xl border border-indigo-100">
            <span className="font-extrabold text-emerald-700 block">2. Realistic / Compatible</span>
            <span className="text-[11px] text-slate-500">Colleges where historical cutoff aligns closely with your rank.</span>
          </div>
          <div className="p-2.5 bg-white rounded-xl border border-indigo-100">
            <span className="font-extrabold text-purple-700 block">3. Safety Cushion</span>
            <span className="text-[11px] text-slate-500">Colleges with significantly higher historical closing cutoffs.</span>
          </div>
        </div>
      </div>

      {/* Loading & Error States */}
      {loading && (
        <div className="text-center py-20 bg-white rounded-2xl border border-slate-200">
          <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm font-semibold text-slate-700">Loading your Option Entry List...</p>
        </div>
      )}

      {error && (
        <div className="p-8 bg-white border border-slate-200 rounded-2xl text-center space-y-3">
          <AlertCircle className="w-10 h-10 text-amber-500 mx-auto" />
          <h3 className="text-base font-bold text-slate-900">Sign in to save your Option Entry List</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            {error}
          </p>
          <div className="pt-2">
            <Link
              to="/login"
              className="px-4 py-2 bg-brand-600 text-white rounded-xl text-xs font-bold inline-block"
            >
              Sign In to DISHA
            </Link>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && items.length === 0 && (
        <div className="p-12 bg-white border border-dashed border-slate-300 rounded-2xl text-center space-y-4">
          <ListTodo className="w-12 h-12 text-slate-300 mx-auto" />
          <div>
            <h3 className="text-lg font-bold text-slate-900">Your Option List is Empty</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
              Start by exploring colleges in the CET Explorer and click "Add to Option List" on compatible branches.
            </p>
          </div>
          <Link
            to="/cet/explore"
            className="px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold inline-flex items-center gap-1.5 shadow-sm"
          >
            <Plus className="w-4 h-4" />
            <span>Discover Compatible Colleges</span>
          </Link>
        </div>
      )}

      {/* Ordered Options List */}
      {!loading && !error && items.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-500 px-2 print:hidden">
            <span>Drag or use arrows to adjust priority hierarchy</span>
            <span>Total Options: <strong>{items.length}</strong></span>
          </div>

          <div className="space-y-2">
            {items.map((item, index) => (
              <div
                key={item.id}
                className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs hover:shadow-sm transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                {/* Priority Number + College Info */}
                <div className="flex items-center gap-4">
                  {/* Priority Pill */}
                  <div className="w-10 h-10 rounded-xl bg-brand-50 border border-brand-200 text-brand-800 flex items-center justify-center font-black text-sm flex-shrink-0">
                    #{item.priority_order}
                  </div>

                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-[10px] font-extrabold border border-slate-200">
                        {item.college_short_name}
                      </span>
                      <span className="text-slate-400 text-xs">•</span>
                      <span className="text-slate-500 text-xs flex items-center gap-1">
                        <MapPin className="w-3 h-3" />
                        {item.city}
                      </span>
                    </div>

                    <h4 className="text-sm font-bold text-slate-900">
                      {item.college_name}
                    </h4>

                    <div className="flex flex-wrap items-center gap-2 pt-0.5">
                      <span className="text-xs font-semibold text-brand-700">
                        {item.branch_name} ({item.branch_code})
                      </span>
                      {item.historical_category && (
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-medium">
                          {item.historical_category}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Priority Shift Buttons & Remove */}
                <div className="flex items-center gap-1.5 self-end sm:self-center print:hidden">
                  <button
                    onClick={() => moveUp(index)}
                    disabled={index === 0}
                    className="p-2 rounded-xl border border-slate-200 hover:bg-slate-50 disabled:opacity-30 disabled:hover:bg-white text-slate-600 transition-colors"
                    title="Move higher in priority"
                  >
                    <ArrowUp className="w-4 h-4" />
                  </button>

                  <button
                    onClick={() => moveDown(index)}
                    disabled={index === items.length - 1}
                    className="p-2 rounded-xl border border-slate-200 hover:bg-slate-50 disabled:opacity-30 disabled:hover:bg-white text-slate-600 transition-colors"
                    title="Move lower in priority"
                  >
                    <ArrowDown className="w-4 h-4" />
                  </button>

                  <button
                    onClick={() => handleRemove(item.id)}
                    className="p-2 rounded-xl border border-slate-200 hover:bg-rose-50 hover:border-rose-200 text-slate-400 hover:text-rose-600 transition-colors ml-2"
                    title="Remove option from list"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom Save Bar */}
          <div className="pt-4 flex justify-end print:hidden">
            <button
              onClick={handleSaveOrder}
              disabled={saving}
              className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 disabled:bg-slate-300 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition-all"
            >
              <Save className="w-4 h-4" />
              <span>{saving ? 'Saving...' : 'Save Reordered Priorities'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
