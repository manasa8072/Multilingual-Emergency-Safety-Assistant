import React from 'react';
import { Send, Sparkles, RotateCcw, AlertCircle } from 'lucide-react';

export default function EmergencyInput({
  inputMessage,
  setInputMessage,
  onAnalyze,
  isLoading,
  error,
  examples = [],
  onSelectExample,
}) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      onAnalyze();
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6 transition-all hover:shadow-md">
      <div className="flex items-center justify-between mb-3">
        <label htmlFor="emergency-text" className="text-base font-bold text-slate-900 flex items-center gap-2">
          <span>Emergency Message Input</span>
          <span className="text-xs font-normal text-slate-500">(Type in English, Tamil, or Tanglish)</span>
        </label>
        {inputMessage && (
          <button
            onClick={() => setInputMessage('')}
            className="text-xs text-slate-400 hover:text-slate-600 flex items-center gap-1 transition-colors"
          >
            <RotateCcw className="w-3 h-3" />
            Clear
          </button>
        )}
      </div>

      {/* Main Textarea */}
      <div className="relative">
        <textarea
          id="emergency-text"
          rows={4}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe your emergency... (e.g. Road la accident aayiduchu near Thoothukudi bus stand, 2 people injured)"
          className={`w-full p-4 text-slate-900 bg-slate-50 border rounded-xl text-sm sm:text-base focus:outline-none focus:ring-2 transition-all resize-y ${
            error
              ? 'border-red-300 focus:ring-red-400 bg-red-50/20'
              : 'border-slate-200 focus:ring-red-500 focus:bg-white'
          }`}
        />
        <div className="flex justify-between items-center text-xs text-slate-400 mt-1 px-1">
          <span>Press Ctrl + Enter to analyze</span>
          <span>{inputMessage.length} characters</span>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-xl text-xs sm:text-sm text-red-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
          <span>{error}</span>
        </div>
      )}

      {/* Action Buttons & Presets */}
      <div className="mt-4 pt-4 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        {/* Quick Example Presets */}
        <div className="space-y-2">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            <span>Quick Test Presets:</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {examples.map((ex) => (
              <button
                key={ex.id}
                type="button"
                onClick={() => onSelectExample(ex.text)}
                className="px-2.5 py-1 text-xs font-medium rounded-lg bg-slate-100 hover:bg-red-50 hover:text-red-700 hover:border-red-200 border border-slate-200 text-slate-700 transition-all text-left"
              >
                {ex.label}
              </button>
            ))}
          </div>
        </div>

        {/* Analyze Button */}
        <button
          onClick={onAnalyze}
          disabled={isLoading}
          className="self-stretch sm:self-end px-6 py-3 bg-red-600 hover:bg-red-700 active:bg-red-800 text-white font-semibold rounded-xl shadow-md shadow-red-200 transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed shrink-0"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Analyze Emergency</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
