import React, { useState, useEffect } from 'react';
import { EmailLog } from '../../types';
import Button from '../common/Button';
import { Mail, Copy, Check } from 'lucide-react';

interface EmailPreviewProps {
  email: EmailLog;
}

const EmailPreview: React.FC<EmailPreviewProps> = ({ email }) => {
  const [copied, setCopied] = useState(false);
  const [bodyText, setBodyText] = useState(email.body || '');

  useEffect(() => {
    setBodyText(email.body || '');
  }, [email]);

  const handleCopy = () => {
    navigator.clipboard.writeText(bodyText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden font-sans">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
        <div className="flex items-center gap-2.5">
          <Mail className="text-brand-500" size={18} />
          <span className="text-[13px] font-bold text-slate-800 tracking-tight leading-none">
            AI Generated Email Draft
          </span>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleCopy} className="gap-1.5 h-8">
            {copied ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </Button>
        </div>
      </div>

      {/* Preview Sheet */}
      <div className="p-6 space-y-4">
        {/* Recipient */}
        <div className="grid grid-cols-[80px_1fr] items-center text-[12px] border-b border-slate-100 pb-3">
          <span className="font-bold text-slate-400 uppercase tracking-wider">To</span>
          <span className="font-semibold text-slate-700">{email.recipient_email}</span>
        </div>

        {/* Subject */}
        <div className="grid grid-cols-[80px_1fr] items-center text-[12px] border-b border-slate-100 pb-3">
          <span className="font-bold text-slate-400 uppercase tracking-wider">Subject</span>
          <span className="font-bold text-slate-800">{email.subject}</span>
        </div>

        {/* Body */}
        <div className="pt-2">
          <textarea
            value={bodyText}
            onChange={(e) => setBodyText(e.target.value)}
            placeholder="AI email body text will appear here..."
            className="w-full text-[13px] text-slate-700 border border-slate-200 bg-slate-50/70 rounded-xl p-4 h-72 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 select-text resize-y leading-relaxed font-medium transition"
          />
        </div>
      </div>
    </div>
  );
};

export default EmailPreview;
