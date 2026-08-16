import React, { useState, useEffect } from 'react';
import { Candidate, CandidateStatus } from '../../types';
import Modal from '../common/Modal';
import Input from '../common/Input';
import Select from '../common/Select';
import Button from '../common/Button';
import { useAppDispatch } from '../../hooks';
import { updateExistingCandidate } from '../../redux/slices/candidateSlice';

interface EditCandidateModalProps {
  isOpen: boolean;
  onClose: () => void;
  candidate: Candidate;
  onSuccess?: () => void;
}

const EditCandidateModal: React.FC<EditCandidateModalProps> = ({
  isOpen,
  onClose,
  candidate,
  onSuccess,
}) => {
  const dispatch = useAppDispatch();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [status, setStatus] = useState<CandidateStatus>('NEW');
  const [skillsInput, setSkillsInput] = useState('');

  useEffect(() => {
    if (candidate) {
      setFirstName(candidate.first_name || '');
      setLastName(candidate.last_name || '');
      setEmail(candidate.email || '');
      setPhone(candidate.phone || '');
      setStatus(candidate.status || 'NEW');

      const skillNames = (candidate.candidate_skills || []).map((cs) => cs.skill.name);
      setSkillsInput(skillNames.join(', '));
    }
  }, [candidate, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!firstName.trim() || !lastName.trim() || !email.trim()) {
      setError('First name, last name, and email are required fields.');
      return;
    }

    setLoading(true);
    setError(null);

    const parsedSkills = skillsInput
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s.length > 0)
      .map((s) => ({ skill_name: s, proficiency: 'Proficient' }));

    const payload = {
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      email: email.trim(),
      phone: phone.trim() || null,
      status: status,
      skills: parsedSkills,
    };

    try {
      const res = await dispatch(updateExistingCandidate({ id: candidate.id, data: payload }));
      if (updateExistingCandidate.fulfilled.match(res)) {
        if (onSuccess) onSuccess();
        onClose();
      } else {
        setError((res.payload as string) || 'Failed to update candidate details.');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred while saving changes.');
    } finally {
      setLoading(false);
    }
  };

  const statusOptions = [
    { value: 'NEW', label: 'New' },
    { value: 'SCREENING', label: 'Screening' },
    { value: 'INTERVIEWING', label: 'Interviewing' },
    { value: 'OFFERED', label: 'Offered' },
    { value: 'HIRED', label: 'Hired' },
    { value: 'REJECTED', label: 'Rejected' },
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Edit Candidate Details"
      size="md"
      footerActions={
        <>
          <Button variant="outline" size="sm" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button variant="primary" size="sm" onClick={handleSubmit} isLoading={loading}>
            Save Changes
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-50 border border-red-100 text-red-600 text-xs p-3 rounded-xl">
            {error}
          </div>
        )}

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="First Name *"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder="John"
            required
          />
          <Input
            label="Last Name *"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            placeholder="Doe"
            required
          />
        </div>

        <Input
          label="Email Address *"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="john.doe@example.com"
          required
        />

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Phone Number"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="+1 555-0199"
          />
          <Select
            label="Application Status"
            options={statusOptions}
            value={status}
            onChange={(e) => setStatus(e.target.value as CandidateStatus)}
          />
        </div>

        <div>
          <Input
            label="Skills (comma-separated)"
            value={skillsInput}
            onChange={(e) => setSkillsInput(e.target.value)}
            placeholder="Python, FastAPI, React, PostgreSQL"
            helperText="Separate multiple skills with commas."
          />
        </div>
      </form>
    </Modal>
  );
};

export default EditCandidateModal;
