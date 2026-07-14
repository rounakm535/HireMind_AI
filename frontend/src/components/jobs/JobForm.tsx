import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Job, JobType, JobStatus } from '../../types';
import Input from '../common/Input';
import Select from '../common/Select';
import Button from '../common/Button';

const jobSchema = z.object({
  title: z.string().min(3, 'Job title must be at least 3 characters'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  requirements: z.string().min(10, 'Requirements must be at least 10 characters'),
  location: z.string().min(2, 'Location must be at least 2 characters'),
  job_type: z.enum(['FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', 'REMOTE'] as const),
  status: z.enum(['DRAFT', 'OPEN', 'CLOSED'] as const),
});

export type JobFormValues = z.infer<typeof jobSchema>;

interface JobFormProps {
  initialValues?: Job;
  onSubmit: (values: JobFormValues) => void;
  isLoading?: boolean;
}

const JobForm: React.FC<JobFormProps> = ({ initialValues, onSubmit, isLoading = false }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<JobFormValues>({
    resolver: zodResolver(jobSchema),
    defaultValues: initialValues
      ? {
          title: initialValues.title,
          description: initialValues.description,
          requirements: initialValues.requirements,
          location: initialValues.location,
          job_type: initialValues.job_type,
          status: initialValues.status,
        }
      : {
          title: '',
          description: '',
          requirements: '',
          location: '',
          job_type: 'FULL_TIME',
          status: 'DRAFT',
        },
  });

  const jobTypeOptions = [
    { value: 'FULL_TIME', label: 'Full Time' },
    { value: 'PART_TIME', label: 'Part Time' },
    { value: 'CONTRACT', label: 'Contract' },
    { value: 'INTERN', label: 'Intern' },
    { value: 'REMOTE', label: 'Remote' },
  ];

  const statusOptions = [
    { value: 'DRAFT', label: 'Draft' },
    { value: 'OPEN', label: 'Open' },
    { value: 'CLOSED', label: 'Closed' },
  ];

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5 bg-white border border-slate-100 rounded-2xl p-6 shadow-sm font-sans max-w-2xl">
      <Input
        label="Job Title"
        id="title"
        placeholder="e.g. Senior Software Engineer"
        error={errors.title?.message}
        {...register('title')}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label="Job Type"
          id="job_type"
          options={jobTypeOptions}
          error={errors.job_type?.message}
          {...register('job_type')}
        />

        <Select
          label="Status"
          id="status"
          options={statusOptions}
          error={errors.status?.message}
          {...register('status')}
        />
      </div>

      <Input
        label="Location"
        id="location"
        placeholder="e.g. San Francisco, CA / Remote"
        error={errors.location?.message}
        {...register('location')}
      />

      <div className="flex flex-col gap-1.5 w-full">
        <label htmlFor="description" className="text-[13px] font-semibold text-slate-700">
          Job Description
        </label>
        <textarea
          id="description"
          placeholder="Provide a detailed job description..."
          className={`w-full text-[13px] text-slate-800 border px-3.5 py-2 rounded-lg bg-white placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 transition h-32 ${
            errors.description ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-slate-200'
          }`}
          {...register('description')}
        />
        {errors.description && <span className="text-[11px] font-semibold text-red-500 mt-0.5">{errors.description.message}</span>}
      </div>

      <div className="flex flex-col gap-1.5 w-full">
        <label htmlFor="requirements" className="text-[13px] font-semibold text-slate-700">
          Job Requirements (Skills, Experience)
        </label>
        <textarea
          id="requirements"
          placeholder="List requirements, e.g. 5+ years Python, FastAPI..."
          className={`w-full text-[13px] text-slate-800 border px-3.5 py-2 rounded-lg bg-white placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 transition h-32 ${
            errors.requirements ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-slate-200'
          }`}
          {...register('requirements')}
        />
        {errors.requirements && <span className="text-[11px] font-semibold text-red-500 mt-0.5">{errors.requirements.message}</span>}
      </div>

      <div className="flex justify-end gap-3 pt-3 border-t border-slate-50">
        <Button type="submit" variant="primary" size="md" isLoading={isLoading}>
          {initialValues ? 'Save Changes' : 'Create Job Post'}
        </Button>
      </div>
    </form>
  );
};

export default JobForm;
