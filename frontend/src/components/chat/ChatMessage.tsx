import React from 'react';
import { Message } from '../../types';
import { Sparkles, User } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

const formatMessageText = (text: string) => {
  const trimmed = text.trim();
  if (trimmed.startsWith('{') && trimmed.endsWith('}')) {
    try {
      const parsed = JSON.parse(trimmed);
      if (parsed.questions && Array.isArray(parsed.questions)) {
        return parsed.questions
          .map(
            (q: any, i: number) =>
              `${i + 1}. **${q.question}**\n   • *Expected Answer*: ${q.expected_answer || 'N/A'}${q.category ? `\n   • *Category*: ${q.category}` : ''}`
          )
          .join('\n\n');
      }
      if (parsed.score !== undefined) {
        return `### 🎯 Candidate Match Assessment\n\n• **Match Score:** ${parsed.score}%\n• **Recommendation:** ${parsed.hiring_recommendation || 'Recommended for technical evaluation'}\n• **Matching Skills:** ${(parsed.matching_skills || []).join(', ') || 'Core engineering competencies'}\n• **Skill Gaps:** ${(parsed.missing_skills || []).join(', ') || 'None identified'}\n• **Experience Match:** ${parsed.experience_match || 'Experience demonstrates required qualifications.'}`;
      }
      if (parsed.missing_skills || parsed.strengths || parsed.priority_skills) {
        return `### 📊 Candidate Skill Gap Analysis\n\n• **Key Strengths:** ${(parsed.strengths || []).join(', ') || 'Solid engineering foundation'}\n• **Priority Skills:** ${(parsed.priority_skills || []).join(', ') || 'Core framework expertise'}\n• **Identified Gaps:** ${(parsed.missing_skills || []).join(', ') || 'None identified'}\n• **Recommended Learning:** ${(parsed.recommended_learning || []).join(', ') || 'Advanced architecture & design patterns'}`;
      }
      if (parsed.subject && parsed.body) {
        return `### 📧 Email Draft\n\n**Subject:** ${parsed.subject}\n\n${parsed.body}`;
      }
      if (Object.keys(parsed).length === 0) {
        return 'Hello! How can I help you evaluate candidates, review skills, or generate interview questions today?';
      }
      return Object.entries(parsed)
        .map(([k, v]) => `• **${k.replace(/_/g, ' ').toUpperCase()}**: ${Array.isArray(v) ? v.join(', ') : String(v)}`)
        .join('\n');
    } catch {
      return text;
    }
  }
  return text;
};

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
        className={`max-w-[75%] rounded-2xl px-4 py-2.5 text-[13px] leading-relaxed shadow-sm border ${
          isAssistant
            ? 'bg-white border-slate-100 text-slate-700'
            : 'bg-brand-600 border-brand-500 text-white shadow-brand-100/10'
        }`}
      >
        <p className="whitespace-pre-wrap select-text font-medium">{formatMessageText(message.text)}</p>
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
