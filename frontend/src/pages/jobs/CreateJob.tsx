import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { createNewJob } from '../../redux/slices/jobSlice';
import PageHeader from '../../components/layout/PageHeader';
import JobForm, { JobFormValues } from '../../components/jobs/JobForm';
import { ArrowLeft } from 'lucide-react';
import Button from '../../components/common/Button';

const CreateJob: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { loading } = useAppSelector((state) => state.jobs);

  const handleSubmit = async (values: JobFormValues) => {
    const result = await dispatch(createNewJob(values));
    if (createNewJob.fulfilled.match(result)) {
      navigate('/jobs');
    }
  };

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Post New Job" subtitle="Create a job description to begin resume matches.">
        <Button variant="outline" size="sm" onClick={() => navigate('/jobs')} className="gap-1.5 h-9">
          <ArrowLeft size={16} />
          <span>Back to List</span>
        </Button>
      </PageHeader>

      {/* Form Container */}
      <JobForm onSubmit={handleSubmit} isLoading={loading} />
    </div>
  );
};

export default CreateJob;
