import { useState } from 'react';
import { useCandidates } from '../../hooks/useCandidates';
import { CandidateTable } from './CandidateTable';
import { AddCandidateModal } from './AddCandidateModal';
import { Toast } from '../ui/Toast';
import type { Candidate } from '../../types/candidate';

const NAV_ITEMS = [
  // hiring-queue.html is served as a static file from publicDir (../Elasticrew-main)
  // so /hiring-queue.html resolves correctly from the Vite dev server at localhost:5173
  { label: 'Hiring Queue',   href: '/hiring-queue.html' },
  // All Candidates is this React SPA — the root path
  { label: 'All Candidates', href: '/', active: true },
  { label: 'Assessments',    href: '/assessments.html' },
  { label: 'Reports',        href: '/reports.html' },
  { label: 'Dashboard',      href: '/dashboard.html' },
  { label: 'Departments',    href: '/departments.html' },
  { label: 'Settings',       href: '/settings.html' },
] as const;

const STAGE_OPTIONS = [
  'Video Screening Pending',
  'Video Screening Completed',
  'MCQ Assessment Pending',
  'MCQ Assessment Completed',
  'Tech Interview Pending',
  'Tech Interview Completed',
  'Hr Interview Pending',
  'Hr Interview Completed',
  'Report Generation Pending',
  'Report Generated',
] as const;

const STATUS_OPTIONS = ['Active', 'On Hold', 'Rejected', 'Hired', 'Withdrawn'] as const;

const DEPARTMENT_OPTIONS = ['Engineering', 'Product', 'Design', 'Sales', 'Operations'] as const;

const SUB_DEPT_OPTIONS = [
  'Frontend',
  'Backend',
  'Full Stack',
  'QA / Testing',
  'UI/UX',
  'Account Executive',
  'HR',
  'Data Science',
] as const;

export function CandidatesPage() {
  const { candidates, total, loading, error, filters, updateFilter, prependCandidate } = useCandidates();
  const [modalOpen, setModalOpen] = useState(false);
  const [toastMsg, setToastMsg] = useState('');

  const handleCandidateAdded = (candidate: Candidate) => {
    prependCandidate(candidate);
    setToastMsg(`\u2713 ${candidate.full_name} has been added successfully!`);
  };

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden', background: '#0E2D7B' }}>
      {/* ── Sidebar ── */}
      <nav className="sidebar" aria-label="Main navigation">
        <div className="sidebar-header">
          <h1 className="sidebar-brand">ElastiCrew</h1>
        </div>
        <ul className="nav-menu">
          {NAV_ITEMS.map(item => (
            <li key={item.href} className={`nav-menu-item${item.active ? ' active' : ''}`}>
              <a href={item.href}>
                <span>{item.label}</span>
              </a>
            </li>
          ))}
        </ul>
        <div className="logout-container">
          <a href="#" className="logout-link">
            <span>Logout</span>
          </a>
        </div>
      </nav>

      {/* ── Main Content ── */}
      <main className="main-content">
        {/* Header */}
        <header className="header-actions">
          <h1 className="page-title">All Candidates</h1>
          <button
            className="btn-add"
            onClick={() => setModalOpen(true)}
            aria-label="Add a new candidate"
          >
            <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
              <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" />
            </svg>
            Add Candidate
          </button>
        </header>

        {/* Candidates section card */}
        <section aria-label="Candidates management">
          {/* Filter Bar */}
          <div className="filter-bar">
            <div className="search-box">
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                aria-hidden="true"
              >
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <input
                type="text"
                placeholder="Search by candidate name..."
                value={filters.search}
                onChange={e => updateFilter('search', e.target.value)}
                aria-label="Search candidates by name"
              />
            </div>
            <div className="filter-group">
              <select
                className="filter-select"
                value={filters.department}
                onChange={e => updateFilter('department', e.target.value)}
                aria-label="Filter by department"
              >
                <option value="all">All Departments</option>
                {DEPARTMENT_OPTIONS.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>

              <select
                className="filter-select"
                value={filters.sub_department}
                onChange={e => updateFilter('sub_department', e.target.value)}
                aria-label="Filter by sub department"
              >
                <option value="all">All Sub Departments</option>
                {SUB_DEPT_OPTIONS.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>

              <select
                className="filter-select"
                value={filters.stage}
                onChange={e => updateFilter('stage', e.target.value)}
                aria-label="Filter by pipeline stage"
              >
                <option value="all">All Stages</option>
                {STAGE_OPTIONS.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>

              <select
                className="filter-select"
                value={filters.status}
                onChange={e => updateFilter('status', e.target.value)}
                aria-label="Filter by status"
              >
                <option value="all">All Statuses</option>
                {STATUS_OPTIONS.map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Error state */}
          {error && (
            <div
              role="alert"
              style={{
                background: '#fef2f2',
                border: '1px solid #fecaca',
                color: '#991b1b',
                padding: '12px 16px',
                borderRadius: 8,
                marginBottom: 16,
                fontSize: 14,
                fontWeight: 600,
              }}
            >
              {error}
            </div>
          )}

          {/* Count row */}
          {!loading && !error && (
            <div
              style={{
                padding: '10px 20px',
                fontSize: 13,
                color: '#64748b',
                fontWeight: 600,
                borderBottom: '1px solid #e2e8f0',
                background: '#fff',
                borderRadius: '12px 12px 0 0',
              }}
            >
              {total} candidate{total !== 1 ? 's' : ''} found
            </div>
          )}

          {/* Table */}
          <CandidateTable candidates={candidates} loading={loading} />
        </section>

        {/* Add Candidate Modal */}
        <AddCandidateModal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          onSuccess={handleCandidateAdded}
        />

        {/* Toast notification */}
        {toastMsg && (
          <Toast message={toastMsg} onDismiss={() => setToastMsg('')} />
        )}
      </main>
    </div>
  );
}
