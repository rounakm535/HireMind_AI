import React from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { sendMessageToAssistant, addMessage, clearChat } from '../../redux/slices/chatSlice';
import PageHeader from '../../components/layout/PageHeader';
import ChatWindow from '../../components/chat/ChatWindow';

const RecruiterChat: React.FC = () => {
  const dispatch = useAppDispatch();
  const { messages, loading } = useAppSelector((state) => state.chat);

  const handleSendMessage = (text: string) => {
    // 1. Add user message locally
    dispatch(
      addMessage({
        id: Math.random().toString(),
        sender: 'user',
        text,
        timestamp: new Date().toISOString(),
      })
    );

    // 2. Dispatch thunk to query AI client
    dispatch(sendMessageToAssistant(text));
  };

  const handleClearChat = () => {
    if (confirm('Clear chat conversation history?')) {
      dispatch(clearChat());
    }
  };

  return (
    <div className="font-sans space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <PageHeader title="AI Recruiter Copilot" subtitle="Ask natural language questions to search through candidates profiles, resumes, and compare fits." />

      {/* Chat Window Panel */}
      <ChatWindow
        messages={messages}
        onSendMessage={handleSendMessage}
        onClearChat={handleClearChat}
        isLoading={loading}
      />
    </div>
  );
};

export default RecruiterChat;
