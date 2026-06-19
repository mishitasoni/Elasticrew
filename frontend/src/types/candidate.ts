export type ExperienceLevel =
  | 'Fresher (0 yrs)'
  | 'Junior (1\u20133 yrs)'
  | 'Mid Level (3\u20135 yrs)'
  | 'Senior (5+ yrs)'
  | 'Lead (10+ yrs)';

export type CandidateStatus = 'Active' | 'On Hold' | 'Rejected' | 'Hired' | 'Withdrawn';

export type PipelineStage =
  | 'Video Screening Pending'
  | 'Video Screening Completed'
  | 'MCQ Assessment Pending'
  | 'MCQ Assessment Completed'
  | 'Tech Interview Pending'
  | 'Tech Interview Completed'
  | 'Hr Interview Pending'
  | 'Hr Interview Completed'
  | 'Report Generation Pending'
  | 'Report Generated';

export interface Candidate {
  id: number;
  full_name: string;
  email: string;
  phone: string;
  experience: ExperienceLevel;
  department: string;
  sub_department: string;
  job_role: string;
  skills: string | null;
  resume_file_name: string | null;
  stage: string;
  status: CandidateStatus;
  remarks: string;
  date_added: string;
  created_at: string;
}

export interface CandidateCreate {
  full_name: string;
  email: string;
  phone: string;
  experience: ExperienceLevel | '';
  department: string;
  sub_department: string;
  job_role: string;
  skills: string;
  resume_file_name: string;
}

export interface CandidateListResponse {
  candidates: Candidate[];
  total: number;
}

export interface FilterState {
  search: string;
  department: string;
  sub_department: string;
  stage: string;
  status: string;
}

export interface ApiError {
  detail: string;
  field?: string;
}

export type FormErrors = Partial<Record<keyof CandidateCreate | 'form', string>>;
