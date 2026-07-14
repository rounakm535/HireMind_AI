import React from 'react';
import { Resume } from '../../types';
import { FileText, Download, ExternalLink } from 'lucide-react';
import Button from '../common/Button';

interface ResumeViewerProps {
  resume: Resume;
}

const ResumeViewer: React.FC<ResumeViewerProps> = ({ resume }) => {
  return (
    <div className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden font-sans h-full flex flex-col">
      {/* Viewer Header */}
      <div className="px-6 py-4 border-b border-slate-50 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <FileText className="text-brand-500" size={18} />
          <span className="text-[13px] font-bold text-slate-800 tracking-tight leading-none">
            {resume.file_name}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <a href={resume.file_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm" className="p-1.5 h-8">
              <ExternalLink size={14} />
            </Button>
          </a>
        </div>
      </div>

      {/* Viewer Body: Render Extracted Text or PDF */}
      <div className="flex-1 bg-slate-50 p-6 overflow-y-auto max-h-[500px]">
        {resume.raw_text ? (
          <pre className="text-[12px] text-slate-600 font-mono leading-relaxed whitespace-pre-wrap select-text">
            {resume.raw_text}
          </pre>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-400">
            <FileText size={36} className="mb-2 text-slate-300" />
            <p className="text-[12px] font-medium">No extracted text context found.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeViewer;
