import React, { useState, useEffect, useRef } from 'react';
import { Message } from '../../types';
import ChatMessage from './ChatMessage';
import Loader from '../common/Loader';
import { Send, Trash2, Sparkles } from 'lucide-react';
import Button from '../common/Button';

interface ChatWindowProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
  onClearChat?: () => void;
  isLoading?: boolean;
}

const QUICK_PROMPTS = [
  '🔍 Find Python developers with FastAPI experience',
  '🏆 Compare the top candidates for Senior AI Engineer',
  '📊 Show candidates with Docker & Kubernetes knowledge',
  '📝 Generate interview questions for Full-Stack Lead',
];

const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  onSendMessage,
  onClearChat,
  isLoading = false,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSend = (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim() || isLoading) return;
    onSendMessage(query.trim());
    setInput('');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSend();
  };

  // Scroll to bottom on updates
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="bg-white border border-slate-100 rounded-2xl shadow-sm flex flex-col h-[650px] overflow-hidden font-sans">
      {/* Chat Header */}
      <div className="px-6 py-4 border-b border-slate-50 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center border border-brand-100">
            <Sparkles size={18} />
          </div>
          <div>
            <h2 className="text-[14px] font-bold text-slate-800 tracking-tight">AI Recruiter Copilot</h2>
            <p className="text-[10px] text-emerald-600 font-bold flex items-center gap-1 mt-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" /> Active & Connected
            </p>
          </div>
        </div>

        {onClearChat && (
          <Button variant="ghost" size="sm" onClick={onClearChat} className="text-slate-400 hover:text-red-500">
            <Trash2 size={15} />
          </Button>
        )}
      </div>

      {/* Messages list pane */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-brand-50 text-brand-500 flex items-center justify-center border border-brand-100 shadow-sm">
              <Sparkles size={24} />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-800">Ask HireMind AI Anything</h3>
              <p className="text-xs text-slate-400 mt-1 max-w-md">
                Search applicants using natural language, compare resumes, filter skills, or draft recruiter communications.
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg w-full pt-2">
              {QUICK_PROMPTS.map((prompt, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSend(prompt)}
                  className="text-left p-3 rounded-xl bg-white border border-slate-200 text-xs font-medium text-slate-700 hover:border-brand-500 hover:text-brand-600 hover:bg-brand-50/30 transition shadow-2xs"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((message) => <ChatMessage key={message.id} message={message} />)
        )}

        {isLoading && (
          <div className="flex gap-3.5 justify-start">
            <div className="w-8 h-8 rounded-lg bg-brand-100 text-brand-600 flex items-center justify-center shrink-0 border border-brand-200">
              <Loader size="xs" />
            </div>
            <div className="bg-white border border-slate-100 rounded-2xl px-4 py-2.5 shadow-sm text-[12px] text-slate-400 font-medium flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-brand-500 animate-ping" />
              <span>HireMind AI Copilot is analyzing query...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts Chip Bar when messages exist */}
      {messages.length > 0 && (
        <div className="px-4 py-2 bg-slate-50 border-t border-slate-100 flex items-center gap-2 overflow-x-auto text-xs no-scrollbar">
          <span className="text-[10px] font-bold text-slate-400 shrink-0 uppercase tracking-wider">Suggestions:</span>
          {QUICK_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSend(prompt)}
              className="px-2.5 py-1 rounded-full bg-white border border-slate-200 text-[11px] font-medium text-slate-600 hover:border-brand-500 hover:text-brand-600 shrink-0 transition"
            >
              {prompt}
            </button>
          ))}
        </div>
      )}

      {/* Input box bottom */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-slate-100 flex gap-3.5 bg-white">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about candidates, skills, or job matches..."
          className="flex-1 text-[13px] border border-slate-200 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition"
        />
        <Button type="submit" variant="primary" size="md" disabled={!input.trim() || isLoading} className="px-5 rounded-xl font-bold">
          <Send size={15} />
        </Button>
      </form>
    </div>
  );
};

export default ChatWindow;
