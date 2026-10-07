import React, { useState } from 'react';
import {
  Globe,
  AlertOctagon,
  Flame,
  Activity,
  Car,
  ShieldAlert,
  UserCheck,
  CloudRain,
  MapPin,
  Users,
  Tag,
  Copy,
  Check,
  Info,
  PhoneCall,
  Clock
} from 'lucide-react';

const CATEGORY_CONFIG = {
  'Medical': {
    icon: Activity,
    color: 'text-rose-600',
    bg: 'bg-rose-50',
    border: 'border-rose-200',
    badge: 'bg-rose-100 text-rose-800'
  },
  'Accident': {
    icon: Car,
    color: 'text-amber-600',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    badge: 'bg-amber-100 text-amber-800'
  },
  'Fire': {
    icon: Flame,
    color: 'text-orange-600',
    bg: 'bg-orange-50',
    border: 'border-orange-200',
    badge: 'bg-orange-100 text-orange-800'
  },
  'Police / Crime': {
    icon: ShieldAlert,
    color: 'text-indigo-600',
    bg: 'bg-indigo-50',
    border: 'border-indigo-200',
    badge: 'bg-indigo-100 text-indigo-800'
  },
  'Personal Safety': {
    icon: UserCheck,
    color: 'text-purple-600',
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    badge: 'bg-purple-100 text-purple-800'
  },
  'Natural Disaster': {
    icon: CloudRain,
    color: 'text-teal-600',
    bg: 'bg-teal-50',
    border: 'border-teal-200',
    badge: 'bg-teal-100 text-teal-800'
  }
};

export default function AnalysisResults({ result }) {
  const [copied, setCopied] = useState(false);

  if (!result || !result.success) return null;

  const {
    user_message,
    language,
    emergency_type,
    urgency,
    extracted_information,
    response,
    model_accuracies_reference
  } = result;

  const catConf = CATEGORY_CONFIG[emergency_type.category] || {
    icon: AlertOctagon,
    color: 'text-red-600',
    bg: 'bg-red-50',
    border: 'border-red-200',
    badge: 'bg-red-100 text-red-800'
  };
  const CategoryIcon = catConf.icon;

  const isHighUrgency = urgency.level.toUpperCase() === 'HIGH';

  const copyReport = () => {
    const reportText = `🚨 EMERGENCY ANALYSIS REPORT
User Message: ${user_message}
Language: ${language.detected} (Confidence: ${language.confidence_percentage}%)
Emergency Type: ${emergency_type.category} (Confidence: ${emergency_type.confidence_percentage}%)
Urgency: ${urgency.level} (Confidence: ${urgency.confidence_percentage}%)
Location: ${extracted_information.location}
People Injured: ${extracted_information.people_injured}
People Affected: ${extracted_information.people_affected}
Keywords: ${extracted_information.keywords.join(', ')}
Recommended Action: ${response.recommended_action}
Safety Note: ${response.disclaimer}`;

    navigator.clipboard.writeText(reportText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-5 animate-in fade-in slide-in-from-bottom-3 duration-300">
      {/* Header Banner with Urgency State */}
      <div
        className={`p-4 sm:p-5 rounded-2xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
          isHighUrgency
            ? 'bg-red-50/80 border-red-300 shadow-sm'
            : 'bg-amber-50/80 border-amber-300 shadow-sm'
        }`}
      >
        <div className="flex items-center gap-3.5">
          <div
            className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 shadow-inner ${
              isHighUrgency ? 'bg-red-600 text-white' : 'bg-amber-500 text-white'
            }`}
          >
            <AlertOctagon className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-600">Emergency Status</span>
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-extrabold tracking-wide uppercase ${
                  isHighUrgency
                    ? 'bg-red-600 text-white ring-2 ring-red-200 animate-pulse'
                    : 'bg-amber-500 text-white ring-2 ring-amber-200'
                }`}
              >
                {urgency.level} URGENCY
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-700 mt-0.5">
              Identified as <strong className="text-slate-900">{emergency_type.category}</strong> incident in{' '}
              <strong className="text-slate-900">{language.detected}</strong>
            </p>
          </div>
        </div>

        <button
          onClick={copyReport}
          className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs sm:text-sm font-semibold text-slate-700 bg-white hover:bg-slate-100 border border-slate-300 rounded-xl shadow-xs transition-colors self-start sm:self-center"
        >
          {copied ? (
            <>
              <Check className="w-4 h-4 text-emerald-600" />
              <span>Copied Report</span>
            </>
          ) : (
            <>
              <Copy className="w-4 h-4 text-slate-500" />
              <span>Copy Structured Report</span>
            </>
          )}
        </button>
      </div>

      {/* Grid of 3 Core Model Classifications */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* 1. Language Card */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider">Language</span>
              <Globe className="w-4 h-4 text-blue-500" />
            </div>
            <div className="text-2xl font-extrabold text-slate-900">{language.detected}</div>
            <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
              <span>Prediction Confidence:</span>
              <span className="font-bold text-slate-800">{language.confidence_percentage}%</span>
            </div>
            {/* Progress bar */}
            <div className="w-full bg-slate-100 rounded-full h-2 mt-1.5 overflow-hidden">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${Math.min(language.confidence_percentage, 100)}%` }}
              />
            </div>
          </div>
          <div className="mt-3 pt-2.5 border-t border-slate-100 text-[11px] text-slate-400">
            Model Test Accuracy: {model_accuracies_reference?.language_test_accuracy ?? 100}%
          </div>
        </div>

        {/* 2. Emergency Type Card */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider">Emergency Type</span>
              <CategoryIcon className={`w-4 h-4 ${catConf.color}`} />
            </div>
            <div className="text-2xl font-extrabold text-slate-900">{emergency_type.category}</div>
            <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
              <span>Prediction Confidence:</span>
              <span className="font-bold text-slate-800">{emergency_type.confidence_percentage}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2 mt-1.5 overflow-hidden">
              <div
                className="bg-red-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${Math.min(emergency_type.confidence_percentage, 100)}%` }}
              />
            </div>
          </div>
          <div className="mt-3 pt-2.5 border-t border-slate-100 text-[11px] text-slate-400">
            Model Test Accuracy: {model_accuracies_reference?.emergency_test_accuracy ?? 81.94}%
          </div>
        </div>

        {/* 3. Urgency Level Card */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-slate-500 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider">Urgency Level</span>
              <AlertOctagon className={`w-4 h-4 ${isHighUrgency ? 'text-red-600' : 'text-amber-500'}`} />
            </div>
            <div
              className={`text-2xl font-extrabold ${
                isHighUrgency ? 'text-red-600' : 'text-amber-600'
              }`}
            >
              {urgency.level.toUpperCase()}
            </div>
            <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
              <span>Prediction Confidence:</span>
              <span className="font-bold text-slate-800">{urgency.confidence_percentage}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2 mt-1.5 overflow-hidden">
              <div
                className={`h-2 rounded-full transition-all duration-500 ${
                  isHighUrgency ? 'bg-red-600' : 'bg-amber-500'
                }`}
                style={{ width: `${Math.min(urgency.confidence_percentage, 100)}%` }}
              />
            </div>
          </div>
          <div className="mt-3 pt-2.5 border-t border-slate-100 text-[11px] text-slate-400">
            Model Test Accuracy: {model_accuracies_reference?.urgency_test_accuracy ?? 87.5}%
          </div>
        </div>
      </div>

      {/* Extracted Information Card */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 mb-4 flex items-center gap-2">
          <span>Extracted Incident Details</span>
          <span className="text-xs font-normal text-slate-500">(Lightweight rule-based extraction)</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Location */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-1">
              <MapPin className="w-4 h-4 text-red-500" />
              <span>Location</span>
            </div>
            <div className="text-base font-bold text-slate-900">
              {extracted_information.location !== 'Not detected' ? (
                <span className="text-slate-900">{extracted_information.location}</span>
              ) : (
                <span className="text-slate-400 italic font-normal">Not detected</span>
              )}
            </div>
          </div>

          {/* People Injured */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-1">
              <Users className="w-4 h-4 text-amber-500" />
              <span>People Injured</span>
            </div>
            <div className="text-base font-bold text-slate-900">
              {extracted_information.people_injured !== 'Not detected' ? (
                <span className="text-red-700 bg-red-100 px-2 py-0.5 rounded-md">
                  {extracted_information.people_injured}
                </span>
              ) : (
                <span className="text-slate-400 italic font-normal">Not detected</span>
              )}
            </div>
          </div>

          {/* People Affected */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-1">
              <Users className="w-4 h-4 text-blue-500" />
              <span>People Affected</span>
            </div>
            <div className="text-base font-bold text-slate-900">
              {extracted_information.people_affected !== 'Not detected' ? (
                <span className="text-blue-700 bg-blue-100 px-2 py-0.5 rounded-md">
                  {extracted_information.people_affected}
                </span>
              ) : (
                <span className="text-slate-400 italic font-normal">Not detected</span>
              )}
            </div>
          </div>
        </div>

        {/* Emergency Trigger Keywords */}
        <div className="mt-4 pt-4 border-t border-slate-100">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-2">
            <Tag className="w-3.5 h-3.5 text-slate-400" />
            <span>Emergency Keywords Detected:</span>
          </div>
          {extracted_information.keywords && extracted_information.keywords.length > 0 ? (
            <div className="flex flex-wrap gap-1.5">
              {extracted_information.keywords.map((kw, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 text-xs font-medium rounded-lg bg-slate-100 text-slate-700 border border-slate-200"
                >
                  {kw}
                </span>
              ))}
            </div>
          ) : (
            <span className="text-xs text-slate-400 italic">None detected</span>
          )}
        </div>
      </div>

      {/* AI Recommended Response Card */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-700 mb-3 flex items-center gap-2">
          <span>AI Recommended Action</span>
        </h3>

        <div className="p-4 rounded-xl bg-slate-900 text-white">
          <div className="text-sm sm:text-base font-medium leading-relaxed">
            {response.recommended_action}
          </div>
        </div>

        {/* Emergency Helpline Contacts */}
        <div className="mt-4">
          <div className="text-xs font-semibold text-slate-500 mb-2 flex items-center gap-1.5">
            <PhoneCall className="w-3.5 h-3.5 text-emerald-600" />
            <span>Emergency Quick Dial Directory:</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {Object.entries(response.emergency_contacts || {}).slice(0, 4).map(([name, num]) => (
              <a
                key={name}
                href={`tel:${num}`}
                className="p-2.5 rounded-xl bg-slate-50 hover:bg-emerald-50 hover:border-emerald-200 border border-slate-200 transition-colors flex items-center justify-between text-xs"
              >
                <span className="text-slate-600 font-medium truncate">{name.replace(' Helpline', '')}</span>
                <span className="font-extrabold text-emerald-700 ml-1">{num}</span>
              </a>
            ))}
          </div>
        </div>

        {/* Safety Disclaimer */}
        <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-2 text-xs text-slate-500">
          <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
          <span>{response.disclaimer}</span>
        </div>
      </div>
    </div>
  );
}
