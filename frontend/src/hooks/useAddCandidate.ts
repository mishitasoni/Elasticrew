import { useState } from 'react';
import { createCandidate } from '../api/candidatesApi';
import type { Candidate, CandidateCreate, FormErrors } from '../types/candidate';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE_RE = /^\+?[\d\s\-()\\.]{7,20}$/;

const EMPTY_FORM: CandidateCreate = {
  full_name: '',
  email: '',
  phone: '',
  experience: '',
  department: '',
  sub_department: '',
  job_role: '',
  skills: '',
  resume_file_name: '',
};

function validate(data: CandidateCreate): FormErrors {
  const errs: FormErrors = {};
  if (!data.full_name.trim()) {
    errs.full_name = 'Full name is required.';
  } else if (data.full_name.trim().length < 2) {
    errs.full_name = 'Name must be at least 2 characters.';
  }
  if (!data.email.trim()) {
    errs.email = 'Email is required.';
  } else if (!EMAIL_RE.test(data.email.trim())) {
    errs.email = 'Enter a valid email address.';
  }
  if (!data.phone.trim()) {
    errs.phone = 'Phone number is required.';
  } else if (!PHONE_RE.test(data.phone.trim())) {
    errs.phone = 'Enter a valid phone number (7\u201320 digits).';
  }
  if (!data.experience) errs.experience = 'Please select an experience level.';
  if (!data.department) errs.department = 'Please select a department.';
  if (!data.sub_department) errs.sub_department = 'Please select a sub department.';
  if (!data.job_role.trim()) errs.job_role = 'Job role is required.';
  return errs;
}

export function useAddCandidate(onSuccess: (c: Candidate) => void) {
  const [form, setForm] = useState<CandidateCreate>(EMPTY_FORM);
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitting, setSubmitting] = useState(false);

  const setField = (key: keyof CandidateCreate, value: string) => {
    setForm(prev => ({ ...prev, [key]: value }));
    if (errors[key]) setErrors(prev => ({ ...prev, [key]: undefined }));
  };

  const reset = () => {
    setForm(EMPTY_FORM);
    setErrors({});
  };

  const submit = async (): Promise<boolean> => {
    const errs = validate(form);
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return false;
    }

    setSubmitting(true);
    setErrors({});
    try {
      const candidate = await createCandidate(form);
      onSuccess(candidate);
      reset();
      return true;
    } catch (err: unknown) {
      const e = err as { message: string; field?: string; status?: number };
      if (e.field) {
        setErrors({ [e.field]: e.message });
      } else {
        setErrors({ form: e.message || 'An unexpected error occurred.' });
      }
      return false;
    } finally {
      setSubmitting(false);
    }
  };

  return { form, errors, submitting, setField, submit, reset };
}
