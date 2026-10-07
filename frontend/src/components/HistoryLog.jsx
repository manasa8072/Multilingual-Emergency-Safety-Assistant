import React from 'react';
import { History, Trash2, ArrowRight } from 'lucide-react';

export default function HistoryLog({ history = [], onSelectHistory, onClearHistory }) {
  if (!history || history.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-slate-500" />
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700">
            Recent Analysis History
          </h3>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-semibold">
            {history.length}
          </span>
        </div>
        <button
          onClick={onClearHistory}
          className="text-xs text-slate-400 hover:text-red-600 flex items-center gap-1 transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Clear History</span>
        </button>
      </div>

      <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
        {history.map((item, index) => (
          <div
            key={index}
            onClick={() => onSelectHistory(item)}
            className="p-3 rounded-xl border border-slate-200/80 bg-slate-50 hover:bg-white hover:border-slate-300 transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs group"
          >
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-semibold text-slate-900 px-1.5 py-0.5 rounded bg-white border border-slate-200">
                  {item.language}
                </span>
                <span className="font-semibold text-slate-800">
                  {item.emergency_type}
                </span>
                <span
                  className={`px-1.5 py-0.5 rounded font-bold uppercase text-[10px] ${
                    item.urgency === 'High'
                      ? 'bg-red-100 text-red-700'
                      : 'bg-amber-100 text-amber-700'
                  }`}
                >
                  {item.urgency}
                </span>
                <span className="text-[10px] text-slate-400 ml-auto sm:ml-0">
                  {item.timestamp}
                </span>
              </div>
              <p className="text-slate-600 truncate">{item.message}</p>
            </div>
            <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-slate-700 shrink-0 self-end sm:self-center transition-transform group-hover:translate-x-0.5" />
          </div>
        ))}
      </div>
    </div>
  );
}
