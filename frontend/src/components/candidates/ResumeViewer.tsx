import React, { useState } from 'react';
import { Resume } from '../../types';
import { FileText, ExternalLink, Eye, AlignLeft } from 'lucide-react';
import Button from '../common/Button';

interface ResumeViewerProps {
  resume: Resume;
}

const ResumeViewer: React.FC<ResumeViewerProps> = ({ resume }) => {
  const [viewMode, setViewMode] = useState<'document' | 'text'>('document');

  // Compute full file URL for PDF iframe preview
  const fileFullUrl = resume.file_url.startsWith('http')
    ? resume.file_url
    : `${window.location.protocol}//${window.location.hostname}:8000${resume.file_url}`;

  const isPdf = resume.file_name.toLowerCase().endsWith('.pdf') || resume.file_url.toLowerCase().includes('.pdf');

  return (
    <div className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden font-sans h-full flex flex-col">
      {/* Viewer Header */}
      <div className="px-6 py-3.5 border-b border-slate-100 flex flex-wrap items-center justify-between gap-3 bg-slate-50/50">
        <div className="flex items-center gap-2.5 min-w-0">
          <FileText className="text-brand-500 shrink-0" size={18} />
          <span className="text-[13px] font-bold text-slate-800 tracking-tight truncate max-w-[220px]">
            {resume.file_name}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Mode Switcher Tabs */}
          <div className="flex bg-slate-200/60 p-0.5 rounded-lg text-[11px] font-bold">
            <button
              type="button"
              onClick={() => setViewMode('document')}
              className={`px-2.5 py-1 rounded-md transition flex items-center gap-1 ${
                viewMode === 'document' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              <Eye size={12} />
              <span>Document</span>
            </button>
            <button
              type="button"
              onClick={() => setViewMode('text')}
              className={`px-2.5 py-1 rounded-md transition flex items-center gap-1 ${
                viewMode === 'text' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              <AlignLeft size={12} />
              <span>Text</span>
            </button>
          </div>

          <a href={fileFullUrl} target="_blank" rel="noopener noreferrer" title="Open original document in new tab">
            <Button variant="outline" size="sm" className="p-1.5 h-8">
              <ExternalLink size={14} />
            </Button>
          </a>
        </div>
      </div>

      {/* Viewer Body */}
      <div className="flex-1 bg-slate-50/60 p-4 min-h-[500px] max-h-[550px] overflow-hidden flex flex-col">
        {viewMode === 'document' ? (
          isPdf ? (
            <iframe
              src={fileFullUrl}
              className="w-full h-full min-h-[480px] rounded-xl border border-slate-200 shadow-inner"
              title={resume.file_name}
            />
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 p-8">
              <FileText size={40} className="mb-2.5 text-slate-300" />
              <p className="text-[13px] font-bold text-slate-700">{resume.file_name}</p>
              <p className="text-[11px] text-slate-400 mt-1 max-w-sm">
                Document preview is optimized for PDF files. Click below to view or download the original file.
              </p>
              <a href={fileFullUrl} target="_blank" rel="noopener noreferrer" className="mt-4">
                <Button variant="outline" size="sm" className="gap-1.5 py-2">
                  <ExternalLink size={14} />
                  <span>Open Original File</span>
                </Button>
              </a>
            </div>
          )
        ) : (
          <div className="h-full overflow-y-auto p-4 bg-white border border-slate-100 rounded-xl">
            {resume.raw_text ? (
              <pre className="text-[12px] text-slate-600 font-mono leading-relaxed whitespace-pre-wrap select-text">
                {resume.raw_text}
              </pre>
            ) : resume.summary ? (
              <div className="space-y-2">
                <p className="text-[11px] font-bold uppercase text-slate-400">Parsed Executive Summary</p>
                <p className="text-[13px] text-slate-600 font-medium leading-relaxed">{resume.summary}</p>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 py-12">
                <FileText size={36} className="mb-2 text-slate-300" />
                <p className="text-[12px] font-medium">No extracted text context found.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeViewer;
