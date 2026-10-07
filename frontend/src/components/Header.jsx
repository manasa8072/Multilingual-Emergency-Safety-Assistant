import React from 'react';
import { ShieldAlert, AlertTriangle } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-red-600 flex items-center justify-center text-white shadow-md shadow-red-200 shrink-0">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 font-heading">
                Multilingual Emergency & Safety Assistant
              </h1>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-red-50 text-red-700 border border-red-200">
                AI Prototype
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-500 font-medium">
              AI-powered emergency understanding for English, Tamil & Tanglish
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3 self-end sm:self-auto">
          <div className="flex items-center gap-1.5 text-xs sm:text-sm text-amber-700 bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200">
            <AlertTriangle className="w-4 h-4 shrink-0 text-amber-600" />
            <span className="font-medium">Dial 112 for real emergencies</span>
          </div>
        </div>
      </div>
    </header>
  );
}
