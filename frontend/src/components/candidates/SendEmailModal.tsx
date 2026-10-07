import React, { useState, useEffect } from 'react';
import { Candidate, Job } from '../../types';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchJobs } from '../../redux/slices/jobSlice';
import { resumeApi } from '../../api/resume';
import Modal from '../common/Modal';
import Button from '../common/Button';
import Input from '../common/Input';
import Select from '../common/Select';
import { Sparkles, Mail, Copy, Check, ExternalLink, Send } from 'lucide-react';

interface SendEmailModalProps {
  isOpen: boolean;
  onClose: () => void;
  candidate: Candidate | null;
}

const SendEmailModal: React.FC<SendEmailModalProps> = ({ isOpen, onClose, candidate }) => {
  const dispatch = useAppDispatch();
  const { jobs } = useAppSelector((state) => state.jobs);

  const [selectedJobId, setSelectedJobId] = useState<string>('');
  const [templateType, setTemplateType] = useState<string>('interview_invitation');
  const [subject, setSubject] = useState<string>('');
  const [body, setBody] = useState<string>('');
  const [generating, setGenerating] = useState(false);
  const [sending, setSending] = useState(false);
  const [copied, setCopied] = useState(false);
  const [sentSuccess, setSentSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const senderEmail = 'hiremindrecruitingteam@gmail.com';

  useEffect(() => {
    if (isOpen) {
      dispatch(fetchJobs({ status: 'OPEN' }));
      setSentSuccess(false);
      setError(null);
      setCopied(false);
    }
  }, [isOpen, dispatch]);

  useEffect(() => {
    if (jobs.length > 0 && !selectedJobId) {
      setSelectedJobId(jobs[0].id);
    }
  }, [jobs, selectedJobId]);

  useEffect(() => {
    if (candidate && jobs.length > 0 && isOpen && !body) {
      handleGenerateDraft(jobs[0]?.id || '', 'interview_invitation');
    }
  }, [candidate, isOpen]);

  const handleGenerateDraft = async (jobIdToUse?: string, templateToUse?: string) => {
    if (!candidate) return;
    const jId = jobIdToUse || selectedJobId || (jobs.length > 0 ? jobs[0].id : '');
    const tType = templateToUse || templateType;
    if (!jId) {
      setError('Please select an associated job opening.');
      return;
    }

    setGenerating(true);
    setError(null);
    try {
      const emailRes = await resumeApi.generateEmail(candidate.id, jId, tType);
      setSubject(emailRes.subject || `Update on your application for ${jobs.find((j: Job) => j.id === jId)?.title || 'Role'}`);
      setBody(emailRes.body || '');
    } catch (err: any) {
      // Fallback draft
      const jobObj = jobs.find((j: Job) => j.id === jId);
      const jTitle = jobObj ? jobObj.title : 'the position';
      setSubject(`Interview Invitation - ${jTitle} | HireMind Recruiting Team`);
      setBody(
        `Dear ${candidate.first_name},\n\nThank you for your interest in the ${jTitle} position. We were very impressed with your profile and would love to invite you for an initial interview.\n\nPlease let us know your availability over the upcoming week.\n\nBest regards,\nHireMind Recruiting Team\nhiremindrecruitingteam@gmail.com`
      );
    } finally {
      setGenerating(false);
    }
  };

  const handleCopy = () => {
    const fullText = `Subject: ${subject}\n\n${body}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handleSend = async () => {
    if (!candidate || !body.trim()) return;
    setSending(true);
    setError(null);
    try {
      await resumeApi.sendEmail({
        candidateId: candidate.id,
        recipientEmail: candidate.email,
        subject: subject || 'Application Update',
        body: body,
      });
      setSentSuccess(true);
      setTimeout(() => {
        onClose();
        setSentSuccess(false);
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to record sent email.');
    } finally {
      setSending(false);
    }
  };

  const templateOptions = [
    { value: 'interview_invitation', label: 'Interview Invitation' },
    { value: 'shortlist', label: 'Shortlist Announcement' },
    { value: 'follow_up', label: 'Follow-up Check-in' },
    { value: 'offer', label: 'Offer Discussion' },
    { value: 'rejection', label: 'Rejection Notification' },
  ];

  const jobOptions = jobs.map((j: Job) => ({ value: j.id, label: j.title }));

  if (!candidate) return null;

  const mailtoUrl = `mailto:${candidate.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Send Email Directly" size="lg">
      <div className="font-sans space-y-4">
        {/* Recipient & Sender Banner */}
        <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-500 uppercase tracking-wider text-[10px]">To:</span>
            <span className="font-bold text-slate-800">
              {candidate.first_name} {candidate.last_name}
            </span>
            <span className="text-slate-400 font-medium">({candidate.email})</span>
          </div>
          <div className="flex items-center gap-1.5 text-slate-500 text-[11px]">
            <span className="text-slate-400">From:</span>
            <span className="font-semibold text-brand-600 bg-brand-50 px-2 py-0.5 rounded-md">{senderEmail}</span>
          </div>
        </div>

        {/* Template & Job Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 items-end">
          <Select
            label="Template Type"
            options={templateOptions}
            value={templateType}
            onChange={(e) => {
              const newType = e.target.value;
              setTemplateType(newType);
              handleGenerateDraft(selectedJobId, newType);
            }}
          />

          <Select
            label="Associated Job Post"
            options={jobOptions.length > 0 ? jobOptions : [{ value: '', label: 'No open jobs available' }]}
            value={selectedJobId}
            onChange={(e) => {
              const newJobId = e.target.value;
              setSelectedJobId(newJobId);
              handleGenerateDraft(newJobId, templateType);
            }}
          />
        </div>

        <div className="flex justify-between items-center pt-1">
          <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Email Content</span>
          <button
            type="button"
            onClick={() => handleGenerateDraft()}
            disabled={generating}
            className="inline-flex items-center gap-1 text-[11px] font-bold text-brand-600 hover:text-brand-700 bg-brand-50 hover:bg-brand-100/70 px-2.5 py-1 rounded-lg transition"
          >
            <Sparkles size={13} className={generating ? 'animate-spin' : ''} />
            <span>{generating ? 'Regenerating...' : 'Regenerate with AI'}</span>
          </button>
        </div>

        {/* Subject */}
        <Input
          label="Subject Line"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="Enter email subject line..."
        />

        {/* Body */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">Message Body</label>
          <textarea
            rows={7}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            className="w-full text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-xl p-3.5 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 leading-relaxed transition resize-y"
            placeholder="Write your email message here..."
          />
        </div>

        {error && <p className="text-xs font-semibold text-red-500">{error}</p>}
        {sentSuccess && (
          <div className="bg-green-50 border border-green-200 text-green-700 text-xs font-bold rounded-xl p-3 flex items-center gap-2">
            <Check size={16} />
            <span>Email sent and logged successfully from {senderEmail}!</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-slate-100">
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={handleCopy} className="gap-1.5 h-9 text-xs">
              {copied ? <Check size={14} className="text-green-600" /> : <Copy size={14} />}
              <span>{copied ? 'Copied!' : 'Copy Text'}</span>
            </Button>
            <a
              href={mailtoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 hover:border-slate-300 rounded-lg text-slate-600 hover:text-slate-800 text-xs font-semibold h-9 transition"
              title="Open draft in your default email application"
            >
              <ExternalLink size={14} />
              <span>Open in Mail App</span>
            </a>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={onClose} className="h-9">
              Cancel
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={handleSend}
              isLoading={sending}
              className="gap-1.5 h-9 font-bold"
            >
              <Send size={14} />
              <span>Send & Log Email</span>
            </Button>
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default SendEmailModal;
