import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Job } from '../../types';
import { jobsApi, GetJobsParams, PaginatedResponse } from '../../api/jobs';

interface JobState {
  jobs: Job[];
  currentJob: Job | null;
  totalJobs: number;
  totalPages: number;
  currentPage: number;
  loading: boolean;
  error: string | null;
}

const initialState: JobState = {
  jobs: [],
  currentJob: null,
  totalJobs: 0,
  totalPages: 0,
  currentPage: 1,
  loading: false,
  error: null,
};

export const fetchJobs = createAsyncThunk(
  'jobs/fetchAll',
  async (params: GetJobsParams, { rejectWithValue }) => {
    try {
      return await jobsApi.getJobs(params);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch jobs');
    }
  }
);

export const fetchJobDetails = createAsyncThunk(
  'jobs/fetchDetails',
  async (id: string, { rejectWithValue }) => {
    try {
      return await jobsApi.getJob(id);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to fetch job details');
    }
  }
);

export const createNewJob = createAsyncThunk(
  'jobs/create',
  async (data: any, { rejectWithValue }) => {
    try {
      return await jobsApi.createJob(data);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to create job');
    }
  }
);

export const updateExistingJob = createAsyncThunk(
  'jobs/update',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await jobsApi.updateJob(id, data);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to update job');
    }
  }
);

export const deleteJobPost = createAsyncThunk(
  'jobs/delete',
  async (id: string, { rejectWithValue }) => {
    try {
      await jobsApi.deleteJob(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error?.message || 'Failed to delete job');
    }
  }
);

const jobSlice = createSlice({
  name: 'jobs',
  initialState,
  reducers: {
    clearCurrentJob: (state) => {
      state.currentJob = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Jobs
      .addCase(fetchJobs.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchJobs.fulfilled, (state, action: PayloadAction<PaginatedResponse<Job>>) => {
        state.loading = false;
        state.jobs = action.payload.items;
        state.totalJobs = action.payload.total;
        state.totalPages = action.payload.pages;
        state.currentPage = action.payload.page;
      })
      .addCase(fetchJobs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch Details
      .addCase(fetchJobDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchJobDetails.fulfilled, (state, action: PayloadAction<Job>) => {
        state.loading = false;
        state.currentJob = action.payload;
      })
      .addCase(fetchJobDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Create
      .addCase(createNewJob.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createNewJob.fulfilled, (state, action: PayloadAction<Job>) => {
        state.loading = false;
        state.jobs.unshift(action.payload);
      })
      .addCase(createNewJob.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Update
      .addCase(updateExistingJob.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateExistingJob.fulfilled, (state, action: PayloadAction<Job>) => {
        state.loading = false;
        state.currentJob = action.payload;
        const index = state.jobs.findIndex((j) => j.id === action.payload.id);
        if (index !== -1) {
          state.jobs[index] = action.payload;
        }
      })
      .addCase(updateExistingJob.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Delete
      .addCase(deleteJobPost.fulfilled, (state, action: PayloadAction<string>) => {
        state.jobs = state.jobs.filter((j) => j.id !== action.payload);
      });
  },
});

export const { clearCurrentJob } = jobSlice.actions;
export default jobSlice.reducer;
