import { useState, useCallback, useEffect } from 'react';
import { getCandidates } from '../api/candidatesApi';
import type { Candidate, FilterState } from '../types/candidate';

const DEFAULT_FILTERS: FilterState = {
  search: '',
  department: 'all',
  sub_department: 'all',
  stage: 'all',
  status: 'all',
};

export function useCandidates() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterState>(DEFAULT_FILTERS);

  const fetchCandidates = useCallback(async (f: FilterState) => {
    setLoading(true);
    setError(null);
    try {
      const res = await getCandidates(f);
      setCandidates(res.candidates);
      setTotal(res.total);
    } catch {
      setError('Failed to load candidates. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCandidates(filters);
  }, [filters, fetchCandidates]);

  const updateFilter = useCallback((key: keyof FilterState, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  }, []);

  const prependCandidate = useCallback((candidate: Candidate) => {
    setCandidates(prev => [candidate, ...prev]);
    setTotal(prev => prev + 1);
  }, []);

  return {
    candidates,
    total,
    loading,
    error,
    filters,
    updateFilter,
    prependCandidate,
    refetch: () => fetchCandidates(filters),
  };
}
