import type { CandidateCreate, CandidateListResponse, Candidate, FilterState } from '../types/candidate';

const BASE = '/api';

export async function getCandidates(filters: FilterState): Promise<CandidateListResponse> {
  const params = new URLSearchParams();
  if (filters.search)         params.set('search', filters.search);
  if (filters.department)     params.set('department', filters.department);
  if (filters.sub_department) params.set('sub_department', filters.sub_department);
  if (filters.stage)          params.set('stage', filters.stage);
  if (filters.status)         params.set('status', filters.status);

  const res = await fetch(`${BASE}/candidates?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch candidates');
  return res.json() as Promise<CandidateListResponse>;
}

export async function createCandidate(payload: CandidateCreate): Promise<Candidate> {
  const res = await fetch(`${BASE}/candidates`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await res.json() as Record<string, unknown>;

  if (!res.ok) {
    // FastAPI validation errors come as { detail: [...] }
    if (res.status === 422 && Array.isArray(data.detail)) {
      const first = (data.detail as Array<{ loc: string[]; msg: string }>)[0];
      const field = first?.loc?.at(-1) as string | undefined;
      throw Object.assign(new Error(first?.msg ?? 'Validation error'), { field, status: 422 });
    }
    // Our custom 409
    throw Object.assign(new Error((data.detail as string) ?? 'Request failed'), {
      field: data.field as string | undefined,
      status: res.status,
    });
  }

  return data as unknown as Candidate;
}
