import React, { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchJobDetails, updateExistingJob, clearCurrentJob } from '../../redux/slices/jobSlice';
import PageHeader from '../../components/layout/PageHeader';
import JobForm, { JobFormValues } from '../../components/jobs/JobForm';
import Loader from '../../components/common/Loader';
import { ArrowLeft } from 'lucide-react';
import Button from '../../components/common/Button';

const EditJob: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { currentJob, loading } = useAppSelector((state) => state.jobs);

  useEffect(() => {
    if (id) {
      dispatch(fetchJobDetails(id));
    }
    return () => {
      dispatch(clearCurrentJob());
    };
  }, [id, dispatch]);

  const handleSubmit = async (values: JobFormValues) => {
    if (id) {
      const result = await dispatch(updateExistingJob({ id, data: values }));
      if (updateExistingJob.fulfilled.match(result)) {
        navigate('/jobs');
      }
    }
  };

  if (loading && !currentJob) {
    return (
      <div className="h-[40vh] w-full flex items-center justify-center">
        <Loader size="lg" className="text-brand-500" />
      </div>
    );
  }

  if (!currentJob) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-400 text-sm">Job post not found.</p>
        <Button variant="primary" size="sm" onClick={() => navigate('/jobs')} className="mt-4">
          Back to list
        </Button>
      </div>
    );
  }

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Edit Job Openings" subtitle={`Make modifications to the post: ${currentJob.title}`}>
        <Button variant="outline" size="sm" onClick={() => navigate('/jobs')} className="gap-1.5 h-9">
          <ArrowLeft size={16} />
          <span>Back to List</span>
        </Button>
      </PageHeader>

      {/* Form Container */}
      <JobForm initialValues={currentJob} onSubmit={handleSubmit} isLoading={loading} />
    </div>
  );
};

export default EditJob;
