import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchCandidates } from '../../redux/slices/candidateSlice';
import { fetchJobs } from '../../redux/slices/jobSlice';
import { resumeApi } from '../../api/resume';
import { EmailLog } from '../../types';
import PageHeader from '../../components/layout/PageHeader';
import Select from '../../components/common/Select';
import Button from '../../components/common/Button';
import EmailPreview from '../../components/emails/EmailPreview';
import Loader from '../../components/common/Loader';
import { Sparkles, Mail, AlertTriangle } from 'lucide-react';

const emailSchema = z.object({
  candidate_id: z.string().min(1, 'Please select a candidate'),
  job_id: z.string().min(1, 'Please select a job'),
  template_type: z.string().min(1, 'Please select a template type'),
});

type EmailFormValues = z.infer<typeof emailSchema>;

const GenerateEmail: React.FC = () => {
  const dispatch = useAppDispatch();
  const { candidates } = useAppSelector((state) => state.candidates);
  const { jobs } = useAppSelector((state) => state.jobs);

  // States
  const [emailResult, setEmailResult] = useState<EmailLog | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    dispatch(fetchCandidates({ size: 100 }));
    dispatch(fetchJobs({ status: 'OPEN' }));
  }, [dispatch]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<EmailFormValues>({
    resolver: zodResolver(emailSchema),
  });

  const onSubmit = async (values: EmailFormValues) => {
    setLoading(true);
    setError(null);
    try {
      const email = await resumeApi.generateEmail(
        values.candidate_id,
        values.job_id,
        values.template_type
      );
      setEmailResult(email);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to generate email template.');
    } finally {
      setLoading(false);
    }
  };

  const templateOptions = [
    { value: '', label: 'Select template type...' },
    { value: 'interview_invitation', label: 'Interview Invitation' },
    { value: 'shortlist', label: 'Shortlist Announcement' },
    { value: 'rejection', label: 'Rejection Notification' },
    { value: 'follow_up', label: 'Follow-up Check-in' },
  ];

  const candidateOptions = [
    { value: '', label: 'Select recipient candidate...' },
    ...candidates.map((c) => ({ value: c.id, label: `${c.first_name} ${c.last_name} (${c.email})` })),
  ];

  const jobOptions = [
    { value: '', label: 'Select associated job...' },
    ...jobs.map((j) => ({ value: j.id, label: j.title })),
  ];

  return (
    <div className="font-sans space-y-6 max-w-5xl">
      {/* Header */}
      <PageHeader title="AI Email Draft Generator" subtitle="Generate professional, personalized candidate emails using AI templates." />

      <div className="grid grid-cols-1 lg:grid-cols-[380px_1fr] gap-6 items-start">
        {/* Left Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm space-y-5">
          <h3 className="text-[14px] font-bold text-slate-800 tracking-tight">Email Parameters</h3>

          <Select
            label="Template Type"
            id="template_type"
            options={templateOptions}
            error={errors.template_type?.message}
            {...register('template_type')}
          />

          <Select
            label="Candidate"
            id="candidate_id"
            options={candidateOptions}
            error={errors.candidate_id?.message}
            {...register('candidate_id')}
          />

          <Select
            label="Associated Job"
            id="job_id"
            options={jobOptions}
            error={errors.job_id?.message}
            {...register('job_id')}
          />

          {error && <span className="text-[11px] font-semibold text-red-500 block">{error}</span>}

          <Button type="submit" variant="primary" className="w-full py-2.5 font-bold gap-1.5 mt-2" isLoading={loading}>
            <Sparkles size={14} className="fill-current" />
            <span>Generate Draft</span>
          </Button>
        </form>

        {/* Right Output Preview */}
        <div>
          {loading ? (
            <div className="bg-white border border-slate-100 rounded-2xl p-12 text-center text-slate-400 flex flex-col items-center justify-center h-64 shadow-sm">
              <Loader size="md" className="text-brand-500 mb-2" />
              <p className="text-xs font-semibold">Generating email template, please wait...</p>
            </div>
          ) : emailResult ? (
            <EmailPreview email={emailResult} />
          ) : (
            <div className="bg-white border border-slate-100 rounded-2xl p-12 text-center text-slate-400 flex flex-col items-center justify-center h-64 shadow-sm">
              <Mail size={32} className="mb-2 text-slate-300" />
              <p className="text-xs font-semibold">No email draft generated yet.</p>
              <p className="text-[10px] text-slate-400 mt-1 max-w-xs">Fill in parameters on the left and trigger generator to view output draft.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GenerateEmail;
