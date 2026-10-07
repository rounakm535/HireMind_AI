import React, { useState, useEffect } from 'react';
import { Candidate } from '../../types';
import { aiApi, CandidateComparisonResult } from '../../api/ai';
import Modal from '../common/Modal';
import Button from '../common/Button';
import Loader from '../common/Loader';
import Badge from '../common/Badge';
import { Sparkles, Trophy, CheckCircle2, AlertTriangle, Send, XCircle } from 'lucide-react';

interface CandidateCompareModalProps {
  isOpen: boolean;
  onClose: () => void;
  candidates: Candidate[];
  onSendEmail?: (candidate: Candidate) => void;
}

const CandidateCompareModal: React.FC<CandidateCompareModalProps> = ({
  isOpen,
  onClose,
  candidates,
  onSendEmail,
}) => {
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<CandidateComparisonResult | null>(null);

  useEffect(() => {
    if (isOpen && candidates.length >= 2) {
      setLoading(true);
      aiApi
        .compareCandidates(candidates)
        .then((res) => setResult(res))
        .catch((err) => {
          console.error('Failed to compare candidates:', err);
        })
        .finally(() => setLoading(false));
    }
  }, [isOpen, candidates]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="AI Side-by-Side Candidate Comparison" maxWidth="max-w-5xl">
      {loading ? (
        <div className="py-20 text-center flex flex-col items-center justify-center space-y-4">
          <Loader size="lg" className="text-brand-500" />
          <div className="space-y-1">
            <h4 className="text-sm font-bold text-slate-800">Analyzing Candidate Profiles...</h4>
            <p className="text-xs text-slate-400">Comparing technical skill alignments, resume match scores, and gap trade-offs.</p>
          </div>
        </div>
      ) : result ? (
        <div className="space-y-6 font-sans">
          {/* Top Recommendation Highlight Banner */}
          <div className="bg-gradient-to-r from-brand-600 to-indigo-700 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
            <div className="absolute right-0 top-0 translate-x-4 -translate-y-4 opacity-10">
              <Trophy size={180} />
            </div>

            <div className="flex items-center gap-2 text-brand-200 text-xs font-bold uppercase tracking-wider mb-2">
              <Sparkles size={14} className="text-amber-300" />
              <span>AI Hiring Recommendation</span>
            </div>

            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h3 className="text-2xl font-black text-white tracking-tight">
                  Top Recommended Pick: <span className="text-amber-300">{result.top_recommendation}</span>
                </h3>
                <p className="text-xs text-brand-100 mt-1 leading-relaxed max-w-2xl font-medium">
                  {result.summary_verdict}
                </p>
              </div>
            </div>
          </div>

          {/* Grid Side-by-Side Cards */}
          <div className={`grid grid-cols-1 md:grid-cols-${Math.min(candidates.length, 3)} gap-5`}>
            {result.comparisons.map((comp, idx) => {
              const candidate = candidates.find(
                (c) => `${c.first_name} ${c.last_name}`.toLowerCase() === comp.candidate_name.toLowerCase()
              ) || candidates[idx];

              const isTop = comp.candidate_name.toLowerCase() === result.top_recommendation.toLowerCase();

              return (
                <div
                  key={idx}
                  className={`bg-white border rounded-2xl p-5 flex flex-col justify-between shadow-sm relative transition ${
                    isTop ? 'border-amber-400 ring-2 ring-amber-400/20 bg-amber-50/10' : 'border-slate-200'
                  }`}
                >
                  {isTop && (
                    <div className="absolute -top-3 right-4 bg-amber-500 text-white text-[10px] font-black uppercase px-2.5 py-0.5 rounded-full shadow-sm flex items-center gap-1">
                      <Trophy size={11} />
                      <span>Best Fit</span>
                    </div>
                  )}

                  <div>
                    <div className="border-b border-slate-100 pb-3 mb-4">
                      <h4 className="text-base font-bold text-slate-800 tracking-tight">{comp.candidate_name}</h4>
                      <p className="text-xs text-slate-400 font-medium mt-0.5">{candidate?.email}</p>

                      <div className="flex items-center gap-2 mt-3">
                        <span className="text-2xl font-black text-brand-600">{comp.fit_score}%</span>
                        <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                          Match Score
                        </span>
                      </div>
                    </div>

                    {/* Strengths */}
                    <div className="space-y-2 mb-4">
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                        <CheckCircle2 size={13} className="text-emerald-500" />
                        Key Strengths
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {comp.key_strengths.map((str, sIdx) => (
                          <Badge key={sIdx} variant="success" className="text-[10px] px-2 py-0.5 font-medium">
                            {str}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Skill Gaps */}
                    <div className="space-y-2 mb-4">
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                        <AlertTriangle size={13} className="text-amber-500" />
                        Missing Skills / Gaps
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {comp.skill_gaps.map((gap, gIdx) => (
                          <Badge key={gIdx} variant="warning" className="text-[10px] px-2 py-0.5 font-medium">
                            {gap}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Verdict */}
                    <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs text-slate-600 font-medium mb-4">
                      <strong className="text-slate-800 block mb-0.5">Recruiter Verdict:</strong>
                      {comp.verdict}
                    </div>
                  </div>

                  {/* Actions */}
                  {candidate && onSendEmail && (
                    <Button
                      variant={isTop ? 'primary' : 'outline'}
                      size="sm"
                      onClick={() => {
                        onClose();
                        onSendEmail(candidate);
                      }}
                      className="w-full gap-1.5 justify-center py-2"
                    >
                      <Send size={13} />
                      <span>Contact {candidate.first_name}</span>
                    </Button>
                  )}
                </div>
              );
            })}
          </div>

          <div className="flex justify-end pt-2 border-t border-slate-100">
            <Button variant="outline" size="sm" onClick={onClose}>
              Close Comparison
            </Button>
          </div>
        </div>
      ) : (
        <div className="py-12 text-center text-slate-400">
          <XCircle size={32} className="mx-auto mb-2 text-slate-300" />
          <p className="text-xs">Unable to perform candidate comparison. Please try again.</p>
        </div>
      )}
    </Modal>
  );
};

export default CandidateCompareModal;
