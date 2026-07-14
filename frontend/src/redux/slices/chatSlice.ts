import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Message } from '../../types';
import { chatApi } from '../../api/chat';

interface ChatState {
  messages: Message[];
  loading: boolean;
  error: string | null;
}

const initialState: ChatState = {
  messages: [
    {
      id: 'welcome',
      sender: 'assistant',
      text: 'Hello! I am HireMind AI, your recruiting copilot. Ask me questions like: "Find Python developers with FastAPI experience" or "Generate interview questions for John Doe".',
      timestamp: new Date().toISOString(),
    },
  ],
  loading: false,
  error: null,
};

export const sendMessageToAssistant = createAsyncThunk(
  'chat/sendMessage',
  async (text: string, { rejectWithValue }) => {
    try {
      const data = await chatApi.sendMessage(text);
      return data.response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Chat service error');
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<Message>) => {
      state.messages.push(action.payload);
    },
    clearChat: (state) => {
      state.messages = [initialState.messages[0]];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessageToAssistant.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessageToAssistant.fulfilled, (state, action: PayloadAction<string>) => {
        state.loading = false;
        state.messages.push({
          id: uuidv4(),
          sender: 'assistant',
          text: action.payload,
          timestamp: new Date().toISOString(),
        });
      })
      .addCase(sendMessageToAssistant.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

// Helper for generating UUID in browser context safely
function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export const { addMessage, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
