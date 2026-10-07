import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import EmergencyInput from './components/EmergencyInput';
import AnalysisResults from './components/AnalysisResults';
import HistoryLog from './components/HistoryLog';

export default function App() {
  const [inputMessage, setInputMessage] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [examples, setExamples] = useState([]);
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem('emergency_assistant_history');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Load presets on mount
  useEffect(() => {
    fetch('/api/examples')
      .then((res) => res.json())
      .then((data) => setExamples(data))
      .catch((err) => console.log('Could not load examples:', err));
  }, []);

  // Save history to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('emergency_assistant_history', JSON.stringify(history));
    } catch (e) {
      console.warn('Failed to save to localStorage:', e);
    }
  }, [history]);

  const handleAnalyze = async () => {
    if (!inputMessage.trim()) {
      setError('Please describe your emergency before analyzing.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputMessage }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        setError(data.error || 'Failed to analyze emergency message.');
        setIsLoading(false);
        return;
      }

      setResult(data);

      // Append to history
      const historyItem = {
        message: inputMessage,
        language: data.language.detected,
        emergency_type: data.emergency_type.category,
        urgency: data.urgency.level,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        fullResult: data,
      };

      setHistory((prev) => [historyItem, ...prev.slice(0, 19)]);
    } catch (err) {
      setError('Connection error: Make sure the FastAPI backend is running on port 8000.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectExample = (text) => {
    setInputMessage(text);
    setError(null);
  };

  const handleSelectHistoryItem = (item) => {
    setInputMessage(item.message);
    if (item.fullResult) {
      setResult(item.fullResult);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleClearHistory = () => {
    setHistory([]);
    localStorage.removeItem('emergency_assistant_history');
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col text-slate-900 font-sans selection:bg-red-500 selection:text-white">
      {/* Header */}
      <Header />

      {/* Main Content Area */}
      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6 sm:space-y-8">
        {/* Input Card */}
        <section aria-label="Emergency Input">
          <EmergencyInput
            inputMessage={inputMessage}
            setInputMessage={setInputMessage}
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
            error={error}
            examples={examples}
            onSelectExample={handleSelectExample}
          />
        </section>

        {/* Results Card */}
        {result && (
          <section aria-label="Analysis Results">
            <AnalysisResults result={result} />
          </section>
        )}

        {/* History Log */}
        {history.length > 0 && (
          <section aria-label="Incident History">
            <HistoryLog
              history={history}
              onSelectHistory={handleSelectHistoryItem}
              onClearHistory={handleClearHistory}
            />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-auto py-5 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 space-y-1">
          <p className="font-medium text-slate-700">
            Multilingual Emergency & Safety Assistant &bull; College AI Demonstration & Research Prototype
          </p>
          <p>
            Supports English, Tamil & Tanglish directly without intermediate translation. Dial 112 for real emergencies.
          </p>
        </div>
      </footer>
    </div>
  );
}
