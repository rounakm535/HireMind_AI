import React, { useState } from 'react';
import { Candidate, MatchScore, InterviewQuestion } from '../../types';
import Badge from '../common/Badge';
import {
  User,
  Mail,
  Phone,
  Calendar,
  Sparkles,
  BookOpen,
  Briefcase,
  AlertTriangle,
  Award,
  HelpCircle,
  Clock,
} from 'lucide-react';

interface CandidateDetailsProps {
  candidate: Candidate;
  matchScore?: MatchScore | null;
  questions?: InterviewQuestion[];
}

const CandidateDetails: React.FC<CandidateDetailsProps> = ({ candidate, matchScore, questions = [] }) => {
  const [activeTab, setActiveTab] = useState<'profile' | 'screening' | 'questions'>('profile');

  const formattedDate = new Date(candidate.created_at).toLocaleDateString(undefined, {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <div className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden font-sans">
      {/* Top Profile Summary Header Banner */}
      <div className="bg-slate-50/50 border-b border-slate-100 p-6 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-brand-100 text-brand-700 rounded-2xl flex items-center justify-center font-bold text-lg border border-brand-200">
            {candidate.first_name[0]}
            {candidate.last_name[0]}
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-800 tracking-tight">
              {candidate.first_name} {candidate.last_name}
            </h2>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[12px] text-slate-400 mt-1 font-semibold">
              <span className="flex items-center gap-1"><Mail size={13} /> {candidate.email}</span>
              {candidate.phone && <span className="flex items-center gap-1"><Phone size={13} /> {candidate.phone}</span>}
              <span className="flex items-center gap-1"><Clock size={13} /> Applied {formattedDate}</span>
            </div>
          </div>
        </div>

        {/* AI Score Badge in Header */}
        {matchScore && (
          <div className="flex items-center gap-4 bg-white border border-slate-100 rounded-xl px-4 py-2.5 shadow-sm">
            <div className="relative flex items-center justify-center">
              <span className="text-[17px] font-black text-brand-600">{Math.round(matchScore.score)}%</span>
            </div>
            <div>
              <p className="text-[10px] font-black uppercase text-slate-400 tracking-wider">AI Fit Score</p>
              <p className="text-[12px] text-slate-600 font-semibold mt-0.5">High Match</p>
            </div>
          </div>
        )}
      </div>

      {/* Tabs Menu */}
      <div className="flex border-b border-slate-100 px-6">
        <button
          onClick={() => setActiveTab('profile')}
          className={`px-4 py-3.5 text-[13px] font-bold border-b-2 transition ${
            activeTab === 'profile'
              ? 'border-brand-500 text-brand-600'
              : 'border-transparent text-slate-400 hover:text-slate-600'
          }`}
        >
          Candidate Profile
        </button>
        <button
          onClick={() => setActiveTab('screening')}
          className={`px-4 py-3.5 text-[13px] font-bold border-b-2 transition ${
            activeTab === 'screening'
              ? 'border-brand-500 text-brand-600'
              : 'border-transparent text-slate-400 hover:text-slate-600'
          }`}
        >
          AI Match Analysis
        </button>
        <button
          onClick={() => setActiveTab('questions')}
          className={`px-4 py-3.5 text-[13px] font-bold border-b-2 transition ${
            activeTab === 'questions'
              ? 'border-brand-500 text-brand-600'
              : 'border-transparent text-slate-400 hover:text-slate-600'
          }`}
        >
          Suggested Questions ({questions.length})
        </button>
      </div>

      {/* Tabs Content */}
      <div className="p-6">
        {/* Tab 1: Profile */}
        {activeTab === 'profile' && (
          <div className="space-y-6">
            {/* Skills */}
            <div>
              <h3 className="text-[13px] font-bold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-2">
                <Award size={15} className="text-brand-500" /> Key Skills
              </h3>
              <div className="flex flex-wrap gap-2">
                {candidate.candidate_skills && candidate.candidate_skills.length > 0 ? (
                  candidate.candidate_skills.map((cs) => (
                    <Badge key={cs.skill.id} variant="brand" className="px-3 py-1 text-xs">
                      {cs.skill.name} {cs.proficiency && `(${cs.proficiency})`}
                    </Badge>
                  ))
                ) : (
                  <span className="text-slate-400 text-xs">No skills associated.</span>
                )}
              </div>
            </div>

            {/* Experience Mockup */}
            <div className="pt-2 border-t border-slate-50">
              <h3 className="text-[13px] font-bold text-slate-700 uppercase tracking-wider mb-4 flex items-center gap-2">
                <Briefcase size={15} className="text-brand-500" /> Work Experience
              </h3>
              <div className="relative pl-6 border-l-2 border-slate-100 space-y-6">
                {/* Stage 1 */}
                <div className="relative">
                  <span className="absolute -left-[31px] top-1.5 w-4 h-4 bg-brand-100 text-brand-600 rounded-full border-4 border-white flex items-center justify-center"></span>
                  <h4 className="text-[13px] font-bold text-slate-800">Senior Software Engineer</h4>
                  <p className="text-[11px] text-slate-400 font-bold">Tech Solutions Corp • 2022 - Present</p>
                  <p className="text-[12px] text-slate-500 mt-2 leading-relaxed font-medium">
                    Led development of API backend systems using Python and FastAPI. Scaled database queries in PostgreSQL, optimizing search and retrieval latency by 40%.
                  </p>
                </div>
                {/* Stage 2 */}
                <div className="relative">
                  <span className="absolute -left-[31px] top-1.5 w-4 h-4 bg-slate-100 text-slate-400 rounded-full border-4 border-white flex items-center justify-center"></span>
                  <h4 className="text-[13px] font-bold text-slate-800">Software Developer</h4>
                  <p className="text-[11px] text-slate-400 font-bold">Innovate Lab • 2020 - 2022</p>
                  <p className="text-[12px] text-slate-500 mt-2 leading-relaxed font-medium">
                    Implemented RESTful routes and schemas validation using Django and Pydantic v1. Configured Redis cache servers and worked within containerized Docker instances.
                  </p>
                </div>
              </div>
            </div>

            {/* Education Mockup */}
            <div className="pt-4 border-t border-slate-50">
              <h3 className="text-[13px] font-bold text-slate-700 uppercase tracking-wider mb-4 flex items-center gap-2">
                <BookOpen size={15} className="text-brand-500" /> Education & Degrees
              </h3>
              <div className="space-y-4">
                <div>
                  <h4 className="text-[13px] font-bold text-slate-800">Bachelor of Science in Computer Science</h4>
                  <p className="text-[11px] text-slate-400 font-bold">State University • Graduation 2020</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Match Analysis */}
        {activeTab === 'screening' && (
          <div className="space-y-6">
            {matchScore ? (
              <>
                {/* Explanation */}
                <div className="bg-slate-50 rounded-xl p-5 border border-slate-100">
                  <h4 className="text-[13px] font-bold text-slate-700 flex items-center gap-2 mb-2.5">
                    <Sparkles size={15} className="text-brand-500" /> AI Executive Analysis
                  </h4>
                  <p className="text-[12px] text-slate-600 leading-relaxed font-medium">
                    {matchScore.fit_explanation || 'No summary explanation generated.'}
                  </p>
                </div>

                {/* Skill Gaps */}
                {matchScore.skill_gap_analysis && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Matched */}
                    <div className="border border-slate-100 rounded-xl p-4 bg-white shadow-sm">
                      <h5 className="text-[12px] font-bold text-green-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-green-500" /> Matched Skills
                      </h5>
                      <div className="flex flex-wrap gap-1.5">
                        {matchScore.skill_gap_analysis.matched_skills.map((s) => (
                          <Badge key={s} variant="success" className="px-2 py-0.5 text-[10px]">
                            {s}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Missing */}
                    <div className="border border-slate-100 rounded-xl p-4 bg-white shadow-sm">
                      <h5 className="text-[12px] font-bold text-red-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-red-500" /> Missing Skills
                      </h5>
                      <div className="flex flex-wrap gap-1.5">
                        {matchScore.skill_gap_analysis.missing_skills.length === 0 ? (
                          <span className="text-slate-400 text-xs font-medium">No missing skills. Perfect match!</span>
                        ) : (
                          matchScore.skill_gap_analysis.missing_skills.map((s) => (
                            <Badge key={s} variant="danger" className="px-2 py-0.5 text-[10px]">
                              {s}
                            </Badge>
                          ))
                        )}
                      </div>
                    </div>

                    {/* Additional */}
                    <div className="border border-slate-100 rounded-xl p-4 bg-white shadow-sm">
                      <h5 className="text-[12px] font-bold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-slate-400" /> Relevant Extras
                      </h5>
                      <div className="flex flex-wrap gap-1.5">
                        {matchScore.skill_gap_analysis.additional_skills.map((s) => (
                          <Badge key={s} variant="slate" className="px-2 py-0.5 text-[10px]">
                            {s}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-12 bg-slate-50 border border-dashed border-slate-200 rounded-2xl">
                <AlertTriangle className="mx-auto text-slate-300 mb-2" size={28} />
                <p className="text-[13px] text-slate-500 font-medium">This candidate has not been screened for a job yet.</p>
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Suggested Questions */}
        {activeTab === 'questions' && (
          <div className="space-y-4">
            {questions.length === 0 ? (
              <div className="text-center py-12 bg-slate-50 border border-dashed border-slate-200 rounded-2xl">
                <HelpCircle className="mx-auto text-slate-300 mb-2" size={28} />
                <p className="text-[13px] text-slate-500 font-medium">No suggested questions available yet.</p>
              </div>
            ) : (
              questions.map((q, idx) => (
                <div key={q.id || idx} className="border border-slate-100 rounded-xl p-4 bg-white shadow-sm font-sans flex gap-3">
                  <div className="w-7 h-7 bg-brand-50 text-brand-600 rounded-full flex items-center justify-center shrink-0 font-bold text-xs mt-0.5">
                    Q
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="text-[13px] font-bold text-slate-800 leading-snug">{q.question}</p>
                      {q.category && (
                        <Badge variant="brand" className="px-1.5 py-0 text-[9px] font-black uppercase">
                          {q.category}
                        </Badge>
                      )}
                    </div>
                    {q.expected_answer && (
                      <div className="mt-2.5 bg-slate-50/50 rounded-lg p-3 border border-slate-100/50">
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-wider">Expected Key Answer</p>
                        <p className="text-[12px] text-slate-500 mt-1 leading-relaxed font-medium">{q.expected_answer}</p>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CandidateDetails;
