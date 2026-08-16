import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Candidate, MatchScore, Resume } from '../../types';
import { candidatesApi, GetCandidatesParams } from '../../api/candidates';
import { resumeApi } from '../../api/resume';
import { PaginatedResponse } from '../../api/jobs';

interface CandidateState {
  candidates: Candidate[];
  currentCandidate: Candidate | null;
  currentMatch: MatchScore | null;
  rankings: MatchScore[];
  totalCandidates: number;
  totalPages: number;
  currentPage: number;
  loading: boolean;
  actionLoading: boolean;
  error: string | null;
}

const initialState: CandidateState = {
  candidates: [],
  currentCandidate: null,
  currentMatch: null,
  rankings: [],
  totalCandidates: 0,
  totalPages: 0,
  currentPage: 1,
  loading: false,
  actionLoading: false,
  error: null,
};

export const fetchCandidates = createAsyncThunk(
  'candidates/fetchAll',
  async (params: GetCandidatesParams, { rejectWithValue }) => {
    try {
      return await candidatesApi.getCandidates(params);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch candidates');
    }
  }
);

export const fetchCandidateDetails = createAsyncThunk(
  'candidates/fetchDetails',
  async (id: string, { rejectWithValue }) => {
    try {
      return await candidatesApi.getCandidate(id);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch candidate details');
    }
  }
);

export const createNewCandidate = createAsyncThunk(
  'candidates/create',
  async (data: any, { rejectWithValue }) => {
    try {
      return await candidatesApi.createCandidate(data);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to create candidate');
    }
  }
);

export const updateExistingCandidate = createAsyncThunk(
  'candidates/update',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await candidatesApi.updateCandidate(id, data);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to update candidate');
    }
  }
);

export const deleteCandidateProfile = createAsyncThunk(
  'candidates/delete',
  async (id: string, { rejectWithValue }) => {
    try {
      await candidatesApi.deleteCandidate(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to delete candidate');
    }
  }
);

export const uploadCandidateResume = createAsyncThunk(
  'candidates/uploadResume',
  async ({ candidateId, file }: { candidateId?: string; file: File }, { rejectWithValue }) => {
    try {
      return await resumeApi.uploadResume(candidateId, file);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to upload resume');
    }
  }
);

export const screenAndMatchResume = createAsyncThunk(
  'candidates/screenAndMatch',
  async ({ resumeId, jobId }: { resumeId: string; jobId: string }, { rejectWithValue }) => {
    try {
      return await resumeApi.matchResume(resumeId, jobId);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'AI resume screening failed');
    }
  }
);

export const fetchJobRankings = createAsyncThunk(
  'candidates/fetchRankings',
  async (jobId: string, { rejectWithValue }) => {
    try {
      return await resumeApi.getJobRankings(jobId);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch rankings');
    }
  }
);

const candidateSlice = createSlice({
  name: 'candidates',
  initialState,
  reducers: {
    clearCurrentCandidate: (state) => {
      state.currentCandidate = null;
      state.currentMatch = null;
    },
    clearCurrentMatch: (state) => {
      state.currentMatch = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch List
      .addCase(fetchCandidates.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCandidates.fulfilled, (state, action: PayloadAction<PaginatedResponse<Candidate>>) => {
        state.loading = false;
        state.candidates = action.payload.items;
        state.totalCandidates = action.payload.total;
        state.totalPages = action.payload.pages;
        state.currentPage = action.payload.page;
      })
      .addCase(fetchCandidates.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch Details
      .addCase(fetchCandidateDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCandidateDetails.fulfilled, (state, action: PayloadAction<Candidate>) => {
        state.loading = false;
        state.currentCandidate = action.payload;
      })
      .addCase(fetchCandidateDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create/Update
      .addCase(createNewCandidate.pending, (state) => {
        state.actionLoading = true;
      })
      .addCase(createNewCandidate.fulfilled, (state, action: PayloadAction<Candidate>) => {
        state.actionLoading = false;
        state.candidates.unshift(action.payload);
      })
      .addCase(createNewCandidate.rejected, (state, action) => {
        state.actionLoading = false;
        state.error = action.payload as string;
      })
      // Resume Upload
      .addCase(uploadCandidateResume.pending, (state) => {
        state.actionLoading = true;
      })
      .addCase(uploadCandidateResume.fulfilled, (state, action: PayloadAction<Resume>) => {
        state.actionLoading = false;
        if (state.currentCandidate && state.currentCandidate.id === action.payload.candidate_id) {
          if (!state.currentCandidate.resumes) {
            state.currentCandidate.resumes = [];
          }
          state.currentCandidate.resumes.unshift(action.payload);
        }
      })
      .addCase(uploadCandidateResume.rejected, (state, action) => {
        state.actionLoading = false;
        state.error = action.payload as string;
      })
      // Screen & Match
      .addCase(screenAndMatchResume.pending, (state) => {
        state.actionLoading = true;
        state.error = null;
      })
      .addCase(screenAndMatchResume.fulfilled, (state, action: PayloadAction<MatchScore>) => {
        state.actionLoading = false;
        state.currentMatch = action.payload;
      })
      .addCase(screenAndMatchResume.rejected, (state, action) => {
        state.actionLoading = false;
        state.error = action.payload as string;
      })
      // Job rankings
      .addCase(fetchJobRankings.fulfilled, (state, action: PayloadAction<MatchScore[]>) => {
        state.rankings = action.payload;
      })
      // Delete
      .addCase(deleteCandidateProfile.fulfilled, (state, action: PayloadAction<string>) => {
        state.candidates = state.candidates.filter((c) => c.id !== action.payload);
      });
  },
});

export const { clearCurrentCandidate, clearCurrentMatch } = candidateSlice.actions;
export default candidateSlice.reducer;
