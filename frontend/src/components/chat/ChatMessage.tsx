import React from 'react';
import { Message } from '../../types';
import { Sparkles, User } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isAssistant = message.sender === 'assistant';

  return (
    <div className={`flex gap-3.5 ${isAssistant ? 'justify-start' : 'justify-end'} font-sans`}>
      {/* Icon Avatar left for assistant */}
      {isAssistant && (
        <div className="w-8 h-8 rounded-lg bg-brand-100 text-brand-600 flex items-center justify-center shrink-0 border border-brand-200">
          <Sparkles size={15} />
        </div>
      )}

      {/* Message Bubble */}
      <div
        className={`max-w-[70%] rounded-2xl px-4 py-2.5 text-[13px] leading-relaxed shadow-sm border ${
          isAssistant
            ? 'bg-white border-slate-100 text-slate-700'
            : 'bg-brand-600 border-brand-500 text-white shadow-brand-100/10'
        }`}
      >
        <p className="whitespace-pre-wrap select-text font-medium">{message.text}</p>
        <span
          className={`block text-[9px] mt-1.5 font-semibold text-right ${
            isAssistant ? 'text-slate-400' : 'text-brand-200'
          }`}
        >
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>

      {/* User Icon right for user */}
      {!isAssistant && (
        <div className="w-8 h-8 rounded-lg bg-slate-100 text-slate-500 flex items-center justify-center shrink-0 border border-slate-200">
          <User size={15} />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
