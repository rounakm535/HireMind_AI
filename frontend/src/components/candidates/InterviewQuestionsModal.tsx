import React, { useState } from 'react';
import { Candidate } from '../../types';
import { aiApi, InterviewQuestionItem } from '../../api/ai';
import Modal from '../common/Modal';
import Button from '../common/Button';
import Loader from '../common/Loader';
import Badge from '../common/Badge';
import { HelpCircle, Sparkles, Copy, Check, Printer, FileText } from 'lucide-react';

interface InterviewQuestionsModalProps {
  isOpen: boolean;
  onClose: () => void;
  candidate: Candidate;
  existingQuestions?: InterviewQuestionItem[];
}

const InterviewQuestionsModal: React.FC<InterviewQuestionsModalProps> = ({
  isOpen,
  onClose,
  candidate,
  existingQuestions,
}) => {
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState<InterviewQuestionItem[]>(existingQuestions || []);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const resumeText = candidate.resumes?.[0]?.raw_text || `${candidate.first_name} ${candidate.last_name} resume`;
      const jobDesc = "Target role screening questions";
      const gaps = candidate.match_scores?.[0]?.skill_gap_analysis || {};

      const res = await aiApi.generateQuestions(jobDesc, resumeText, gaps);
      setQuestions(res.questions || []);
    } catch (err) {
      console.error('Failed to generate interview questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    const text = questions
      .map(
        (q, idx) =>
          `Q${idx + 1} [${q.category} - ${q.difficulty_level}]: ${q.question}\nExpected Evaluation: ${q.expected_answer}\n`
      )
      .join('\n');
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Interview Preparation Questionnaire - ${candidate.first_name} ${candidate.last_name}`} maxWidth="max-w-3xl">
      <div className="space-y-5 font-sans">
        {/* Header bar */}
        <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-brand-50 text-brand-600 p-2 rounded-lg">
              <Sparkles size={18} />
            </div>
            <div>
              <h4 className="text-xs font-bold text-slate-800">Tailored Technical Interview Questions</h4>
              <p className="text-[11px] text-slate-400">Custom generated questions targeting candidate skill gap areas.</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {questions.length > 0 && (
              <Button variant="outline" size="sm" onClick={copyToClipboard} className="gap-1.5 h-8 text-xs">
                {copied ? <Check size={13} className="text-emerald-500" /> : <Copy size={13} />}
                <span>{copied ? 'Copied!' : 'Copy Sheet'}</span>
              </Button>
            )}

            <Button
              variant="primary"
              size="sm"
              onClick={handleGenerate}
              isLoading={loading}
              className="gap-1.5 h-8 text-xs"
            >
              <Sparkles size={13} />
              <span>{questions.length > 0 ? 'Regenerate' : 'Generate Questions'}</span>
            </Button>
          </div>
        </div>

        {/* Questions list */}
        {loading ? (
          <div className="py-16 text-center flex flex-col items-center justify-center space-y-3">
            <Loader size="lg" className="text-brand-500" />
            <p className="text-xs font-semibold text-slate-500">Generating tailored interview questions...</p>
          </div>
        ) : questions.length > 0 ? (
          <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-1">
            {questions.map((item, idx) => (
              <div key={idx} className="bg-white border border-slate-100 rounded-xl p-4 space-y-2 shadow-xs">
                <div className="flex items-start justify-between gap-3">
                  <span className="text-xs font-extrabold text-brand-600 shrink-0">Q{idx + 1}.</span>
                  <h5 className="text-xs font-bold text-slate-800 flex-1 leading-snug">{item.question}</h5>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <Badge variant="brand" className="text-[10px] px-2 py-0.5">
                      {item.category}
                    </Badge>
                    <Badge variant="slate" className="text-[10px] px-2 py-0.5">
                      {item.difficulty_level}
                    </Badge>
                  </div>
                </div>

                <div className="bg-slate-50/70 rounded-lg p-3 text-[11px] text-slate-600 border border-slate-100">
                  <strong className="text-slate-800 block mb-0.5 font-bold">Ideal Candidate Answer Rubric:</strong>
                  <p className="leading-relaxed text-slate-600">{item.expected_answer}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-12 text-center text-slate-400 bg-white border border-slate-100 rounded-xl space-y-2">
            <FileText size={28} className="mx-auto text-slate-300" />
            <p className="text-xs font-medium">No interview questions generated yet.</p>
            <p className="text-[11px] text-slate-400">Click "Generate Questions" above to create an AI screening sheet.</p>
          </div>
        )}

        <div className="flex justify-end pt-3 border-t border-slate-100">
          <Button variant="outline" size="sm" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default InterviewQuestionsModal;
