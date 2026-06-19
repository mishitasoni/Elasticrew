import { useEffect, useRef, useState } from 'react';
import { useAddCandidate } from '../../hooks/useAddCandidate';
import type { Candidate } from '../../types/candidate';

interface AddCandidateModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (candidate: Candidate) => void;
}

const EXPERIENCE_OPTIONS = [
  'Fresher (0 yrs)',
  'Junior (1\u20133 yrs)',
  'Mid Level (3\u20135 yrs)',
  'Senior (5+ yrs)',
  'Lead (10+ yrs)',
] as const;

const DEPARTMENT_OPTIONS = [
  'Engineering',
  'Product',
  'Design',
  'Sales',
  'Operations',
] as const;

const SUB_DEPARTMENT_OPTIONS = [
  'Frontend',
  'Backend',
  'Full Stack',
  'QA / Testing',
  'UI/UX',
  'Account Executive',
  'HR',
  'Data Science',
] as const;

export function AddCandidateModal({ isOpen, onClose, onSuccess }: AddCandidateModalProps) {
  const [successMsg, setSuccessMsg] = useState('');

  const handleSuccess = (candidate: Candidate) => {
    setSuccessMsg(`\u2713 ${candidate.full_name} added successfully!`);
    setTimeout(() => {
      setSuccessMsg('');
      onSuccess(candidate);
      onClose();
    }, 900);
  };

  const { form, errors, submitting, setField, submit, reset } = useAddCandidate(handleSuccess);

  const firstInputRef = useRef<HTMLInputElement>(null);

  // Focus first input when modal opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => firstInputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  // Reset form when modal closes
  useEffect(() => {
    if (!isOpen) {
      reset();
      setSuccessMsg('');
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  // Prevent body scroll while open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await submit();
  };

  const inputStyle = (hasError: boolean): React.CSSProperties => ({
    width: '100%',
    padding: '10px 12px',
    border: `1px solid ${hasError ? '#ef4444' : '#e2e8f0'}`,
    borderRadius: 8,
    fontSize: 14,
    fontWeight: 500,
    color: '#0f172a',
    background: hasError ? '#fff8f8' : '#f8fafc',
    outline: 'none',
    boxSizing: 'border-box',
    fontFamily: 'Outfit, -apple-system, sans-serif',
    boxShadow: hasError ? '0 0 0 3px rgba(239,68,68,0.12)' : 'none',
    transition: 'border-color 0.2s, box-shadow 0.2s',
  });

  const labelStyle: React.CSSProperties = {
    display: 'block',
    fontSize: 13,
    fontWeight: 700,
    marginBottom: 6,
    color: '#0f172a',
  };

  const fieldGroupStyle: React.CSSProperties = { marginBottom: 0 };

  const errorSpanStyle: React.CSSProperties = {
    display: 'block',
    fontSize: 11.5,
    fontWeight: 600,
    color: '#dc2626',
    marginTop: 4,
    minHeight: 16,
  };

  const hintSpanStyle: React.CSSProperties = {
    display: 'block',
    fontSize: 11.5,
    color: '#94a3b8',
    marginTop: 4,
  };

  return (
    <div
      className={`modal-overlay${isOpen ? ' active' : ''}`}
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="add-candidate-title"
    >
      <div className="modal-card add-candidate-modal-card">
        {/* ── Header ── */}
        <div className="modal-header-row">
          <h2 className="modal-header" id="add-candidate-title" style={{ marginBottom: 0 }}>
            Add New Candidate
          </h2>
          <button
            type="button"
            className="modal-close-x"
            aria-label="Close dialog"
            onClick={onClose}
          >
            &times;
          </button>
        </div>

        {/* ── Error banner ── */}
        {errors.form && (
          <div className="form-error-banner" role="alert">
            {errors.form}
          </div>
        )}

        {/* ── Success banner ── */}
        {successMsg && (
          <div className="form-success-banner" role="status">
            {successMsg}
          </div>
        )}

        {/* ── Form ── */}
        <form
          id="addCandidateForm"
          className="modal-scrollable-form"
          noValidate
          onSubmit={handleSubmit}
        >
          {/* Row 1: Full Name + Email */}
          <div className="form-row-2col">
            <div style={fieldGroupStyle}>
              <label htmlFor="ac-fullName" style={labelStyle}>
                Full Name <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                id="ac-fullName"
                ref={firstInputRef}
                type="text"
                placeholder="e.g. Jane Doe"
                autoComplete="off"
                value={form.full_name}
                onChange={e => setField('full_name', e.target.value)}
                style={inputStyle(!!errors.full_name)}
                aria-describedby="err-fullName"
                aria-invalid={!!errors.full_name}
              />
              <span id="err-fullName" style={errorSpanStyle}>{errors.full_name ?? ''}</span>
            </div>

            <div style={fieldGroupStyle}>
              <label htmlFor="ac-email" style={labelStyle}>
                Email Address <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                id="ac-email"
                type="email"
                placeholder="e.g. jane@company.com"
                autoComplete="off"
                value={form.email}
                onChange={e => setField('email', e.target.value)}
                style={inputStyle(!!errors.email)}
                aria-describedby="err-email"
                aria-invalid={!!errors.email}
              />
              <span id="err-email" style={errorSpanStyle}>{errors.email ?? ''}</span>
            </div>
          </div>

          {/* Row 2: Phone + Experience */}
          <div className="form-row-2col">
            <div style={fieldGroupStyle}>
              <label htmlFor="ac-phone" style={labelStyle}>
                Phone Number <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <input
                id="ac-phone"
                type="tel"
                placeholder="e.g. +91 9876543210"
                autoComplete="off"
                value={form.phone}
                onChange={e => setField('phone', e.target.value)}
                style={inputStyle(!!errors.phone)}
                aria-describedby="err-phone"
                aria-invalid={!!errors.phone}
              />
              <span id="err-phone" style={errorSpanStyle}>{errors.phone ?? ''}</span>
            </div>

            <div style={fieldGroupStyle}>
              <label htmlFor="ac-experience" style={labelStyle}>
                Experience <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <select
                id="ac-experience"
                value={form.experience}
                onChange={e => setField('experience', e.target.value)}
                style={inputStyle(!!errors.experience)}
                aria-describedby="err-experience"
                aria-invalid={!!errors.experience}
              >
                <option value="" disabled>Select experience level</option>
                {EXPERIENCE_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
              <span id="err-experience" style={errorSpanStyle}>{errors.experience ?? ''}</span>
            </div>
          </div>

          {/* Row 3: Department + Sub Department */}
          <div className="form-row-2col">
            <div style={fieldGroupStyle}>
              <label htmlFor="ac-department" style={labelStyle}>
                Department <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <select
                id="ac-department"
                value={form.department}
                onChange={e => setField('department', e.target.value)}
                style={inputStyle(!!errors.department)}
                aria-describedby="err-department"
                aria-invalid={!!errors.department}
              >
                <option value="" disabled>Select Department</option>
                {DEPARTMENT_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
              <span id="err-department" style={errorSpanStyle}>{errors.department ?? ''}</span>
            </div>

            <div style={fieldGroupStyle}>
              <label htmlFor="ac-subDepartment" style={labelStyle}>
                Sub Department <span style={{ color: '#ef4444' }}>*</span>
              </label>
              <select
                id="ac-subDepartment"
                value={form.sub_department}
                onChange={e => setField('sub_department', e.target.value)}
                style={inputStyle(!!errors.sub_department)}
                aria-describedby="err-subDept"
                aria-invalid={!!errors.sub_department}
              >
                <option value="" disabled>Select Sub Department</option>
                {SUB_DEPARTMENT_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
              <span id="err-subDept" style={errorSpanStyle}>{errors.sub_department ?? ''}</span>
            </div>
          </div>

          {/* Job Role — full width */}
          <div style={fieldGroupStyle}>
            <label htmlFor="ac-jobRole" style={labelStyle}>
              Job Role <span style={{ color: '#ef4444' }}>*</span>
            </label>
            <input
              id="ac-jobRole"
              type="text"
              placeholder="e.g. Senior Backend Engineer"
              autoComplete="off"
              value={form.job_role}
              onChange={e => setField('job_role', e.target.value)}
              style={inputStyle(!!errors.job_role)}
              aria-describedby="err-jobRole"
              aria-invalid={!!errors.job_role}
            />
            <span id="err-jobRole" style={errorSpanStyle}>{errors.job_role ?? ''}</span>
          </div>

          {/* Skills — full width, optional */}
          <div style={fieldGroupStyle}>
            <label htmlFor="ac-skills" style={labelStyle}>Skills</label>
            <input
              id="ac-skills"
              type="text"
              placeholder="e.g. React, Node.js, PostgreSQL"
              value={form.skills}
              onChange={e => setField('skills', e.target.value)}
              style={inputStyle(false)}
            />
            <span style={hintSpanStyle}>Optional — separate with commas</span>
          </div>

          {/* Resume File Name — full width, optional */}
          <div style={fieldGroupStyle}>
            <label htmlFor="ac-resumeFileName" style={labelStyle}>Resume File Name</label>
            <input
              id="ac-resumeFileName"
              type="text"
              placeholder="e.g. jane_resume.pdf"
              value={form.resume_file_name}
              onChange={e => setField('resume_file_name', e.target.value)}
              style={inputStyle(false)}
            />
            <span style={hintSpanStyle}>Optional — e.g. jane_resume.pdf</span>
          </div>

          {/* ── Actions ── */}
          <div className="modal-actions">
            <button
              type="button"
              className="btn-secondary"
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-submit"
              disabled={submitting || !!successMsg}
              style={{ minWidth: 140, justifyContent: 'center' }}
            >
              {submitting ? (
                <>
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2.5"
                    style={{ animation: 'spin 0.8s linear infinite' }}
                    aria-hidden="true"
                  >
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
                  </svg>
                  Saving...
                </>
              ) : (
                'Add Candidate'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
