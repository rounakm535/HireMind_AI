import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { createNewCandidate, uploadCandidateResume } from '../../redux/slices/candidateSlice';
import PageHeader from '../../components/layout/PageHeader';
import Input from '../../components/common/Input';
import Button from '../../components/common/Button';
import { UploadCloud, FileText, X, Sparkles } from 'lucide-react';

const uploadSchema = z.object({
  first_name: z.string().optional(),
  last_name: z.string().optional(),
  email: z.string().email('Please enter a valid email address').or(z.literal('')).optional(),
  phone: z.string().optional(),
});

type UploadFormValues = z.infer<typeof uploadSchema>;

const UploadResume: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { actionLoading, error } = useAppSelector((state) => state.candidates);

  // States
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UploadFormValues>({
    resolver: zodResolver(uploadSchema),
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.type !== 'application/pdf' && selectedFile.name.split('.').pop() !== 'docx') {
        setFileError('Only PDF and DOCX files are allowed.');
        setFile(null);
      } else {
        setFileError(null);
        setFile(selectedFile);
      }
    }
  };

  const onSubmit = async (values: UploadFormValues) => {
    if (!file) {
      setFileError('Please select a resume file to upload.');
      return;
    }

    let candidateId: string | undefined = undefined;

    // If user explicitly filled out manual info, create candidate profile first
    if (values.first_name?.trim() || values.last_name?.trim() || values.email?.trim()) {
      const candidateResult = await dispatch(
        createNewCandidate({
          first_name: values.first_name?.trim() || 'Applicant',
          last_name: values.last_name?.trim() || 'Candidate',
          email: values.email?.trim() || `applicant_${Math.random().toString(36).substring(2, 9)}@extracted.com`,
          phone: values.phone?.trim() || undefined,
        })
      );
      if (createNewCandidate.fulfilled.match(candidateResult)) {
        candidateId = candidateResult.payload.id;
      } else {
        return;
      }
    }

    // Step 2: Upload file and trigger resume parsing (backend will auto-extract and populate details)
    const uploadResult = await dispatch(
      uploadCandidateResume({ candidateId, file })
    );

    if (uploadCandidateResume.fulfilled.match(uploadResult)) {
      const createdResume = uploadResult.payload;
      const targetCandidateId = candidateId || createdResume.candidate_id;
      if (targetCandidateId) {
        navigate(`/candidates/${targetCandidateId}`);
      } else {
        navigate('/candidates');
      }
    }
  };

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Upload Candidate Resume" subtitle="Upload a resume to automatically extract candidate details, skills, experience, and education." />

      <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-6 items-start max-w-5xl">
        {/* Left Side: Candidate profile input form */}
        <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm space-y-5">
          <div>
            <h3 className="text-[14px] font-bold text-slate-800 tracking-tight">Candidate Profile Information</h3>
            <p className="text-[11px] text-slate-400 font-medium mt-0.5">
              Enter details manually or leave empty to auto-extract candidate name, email, phone, experience & skills directly from the resume file.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="First Name"
              id="first_name"
              placeholder="e.g. Alice (or auto-extract)"
              error={errors.first_name?.message}
              {...register('first_name')}
            />
            <Input
              label="Last Name"
              id="last_name"
              placeholder="e.g. Smith (or auto-extract)"
              error={errors.last_name?.message}
              {...register('last_name')}
            />
          </div>

          <Input
            label="Email Address"
            id="email"
            placeholder="alice.smith@example.com (or auto-extract)"
            error={errors.email?.message}
            {...register('email')}
          />

          <Input
            label="Phone Number"
            id="phone"
            placeholder="+1 (555) 0123 (or auto-extract)"
            error={errors.phone?.message}
            {...register('phone')}
          />
        </div>

        {/* Right Side: File Upload Drop Area */}
        <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex flex-col gap-4">
          <h3 className="text-[14px] font-bold text-slate-800 tracking-tight">Resume Document</h3>

          {/* File Picker card */}
          {!file ? (
            <div className="border-2 border-dashed border-slate-200 hover:border-brand-400 bg-slate-50/50 rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer relative group transition">
              <input
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                className="absolute inset-0 opacity-0 cursor-pointer"
              />
              <UploadCloud size={32} className="text-slate-400 group-hover:text-brand-500 transition mb-3" />
              <p className="text-[12px] font-bold text-slate-700 leading-tight">Drag and drop file here</p>
              <p className="text-[10px] text-slate-400 font-medium mt-1">Accepts PDF, DOCX up to 10MB</p>
            </div>
          ) : (
            <div className="border border-brand-100 bg-brand-50/20 rounded-xl p-4 flex items-center justify-between gap-3">
              <div className="flex items-center gap-2.5 min-w-0">
                <FileText size={20} className="text-brand-500 shrink-0" />
                <div className="min-w-0">
                  <p className="text-[12px] font-bold text-slate-800 truncate">{file.name}</p>
                  <p className="text-[10px] text-slate-400 mt-0.5">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setFile(null)}
                className="p-1 hover:bg-slate-100 text-slate-400 hover:text-slate-600 rounded-md transition"
              >
                <X size={15} />
              </button>
            </div>
          )}

          {fileError && <span className="text-[11px] font-semibold text-red-500">{fileError}</span>}
          {error && <span className="text-[11px] font-semibold text-red-500">{error}</span>}

          <Button
            type="submit"
            variant="primary"
            className="w-full py-2.5 font-bold gap-1.5 mt-2"
            isLoading={actionLoading}
          >
            <Sparkles size={14} className="fill-current" />
            <span>Upload and Screen</span>
          </Button>
        </div>
      </form>
    </div>
  );
};

export default UploadResume;
