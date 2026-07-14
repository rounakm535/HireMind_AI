import React, { useState, useEffect, useRef } from 'react';
import { Message } from '../../types';
import ChatMessage from './ChatMessage';
import Loader from '../common/Loader';
import { Send, Trash2 } from 'lucide-react';
import Button from '../common/Button';

interface ChatWindowProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
  onClearChat?: () => void;
  isLoading?: boolean;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  onSendMessage,
  onClearChat,
  isLoading = false,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput('');
  };

  // Scroll to bottom on updates
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="bg-white border border-slate-100 rounded-2xl shadow-sm flex flex-col h-[600px] overflow-hidden font-sans">
      {/* Chat Header */}
      <div className="px-6 py-4 border-b border-slate-50 flex items-center justify-between">
        <div>
          <h2 className="text-[14px] font-bold text-slate-800 tracking-tight">AI Recruiter Assistant</h2>
          <p className="text-[10px] text-green-500 font-bold flex items-center gap-1 mt-0.5">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" /> Online
          </p>
        </div>

        {onClearChat && (
          <Button variant="ghost" size="sm" onClick={onClearChat} className="text-slate-400 hover:text-red-500">
            <Trash2 size={15} />
          </Button>
        )}
      </div>

      {/* Messages list pane */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50 space-y-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex gap-3.5 justify-start">
            <div className="w-8 h-8 rounded-lg bg-brand-100 text-brand-600 flex items-center justify-center shrink-0 border border-brand-200">
              <Loader size="xs" />
            </div>
            <div className="bg-white border border-slate-100 rounded-2xl px-4 py-2.5 shadow-sm text-[12px] text-slate-400 font-medium">
              HireMind is typing...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input box bottom */}
      <form onSubmit={handleSend} className="p-4 border-t border-slate-50 flex gap-3.5 bg-white">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about candidates, skills, or job matches..."
          className="flex-1 text-[13px] border border-slate-200 rounded-lg px-4 py-2 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 transition"
        />
        <Button type="submit" variant="primary" size="md" disabled={!input.trim() || isLoading} className="px-4">
          <Send size={15} />
        </Button>
      </form>
    </div>
  );
};

export default ChatWindow;
