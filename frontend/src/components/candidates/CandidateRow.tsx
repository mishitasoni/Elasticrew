import React, { useState } from 'react';
import type { Candidate, CandidateStatus } from '../../types/candidate';

interface CandidateRowProps {
  candidate: Candidate;
}

function getStageBadgeClass(stage: string): string {
  const lower = stage.toLowerCase();
  if (lower.includes('completed') || lower.includes('reviewed')) return 'shortlisted';
  if (lower.includes('pending') || lower.includes('abandoned')) return 'screening';
  return 'screening';
}

function getStatusClass(status: CandidateStatus | string): string {
  switch (status) {
    case 'Active':    return 'status-active';
    case 'On Hold':   return 'status-onhold';
    case 'Rejected':  return 'status-rejected';
    case 'Hired':     return 'status-hired';
    case 'Withdrawn': return 'status-withdrawn';
    default:          return 'status-active';
  }
}

const STATUS_OPTIONS: CandidateStatus[] = ['Active', 'On Hold', 'Rejected', 'Hired', 'Withdrawn'];

const ACTION_OPTIONS = [
  { value: 'video', label: 'Send Video Bot Invite' },
  { value: 'mcq',   label: 'Send MCQ Assessment Invite' },
  { value: 'tech',  label: 'Send Technical Interview Invite' },
  { value: 'hr',    label: 'Send HR Interview Invite' },
  { value: 'delete', label: 'Delete Candidate' },
];

export function CandidateRow({ candidate }: CandidateRowProps) {
  const stageBadgeClass = getStageBadgeClass(candidate.stage);
  const [actionValue, setActionValue] = useState('');

  // Async function to handle api deletion
  const deleteCandidate = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/candidates/${candidate.id}`,
        {
          method: 'DELETE',
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Delete failed');
      }

      alert('Candidate deleted successfully');
      window.location.reload();
    } catch (error) {
      console.error(error);
      alert(
        error instanceof Error
          ? error.message
          : 'Failed to delete candidate'
      );
    }
  };

  const handleActionChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    if (!value) return;

    if (value === 'delete') {
      const confirmed = window.confirm(
        `Delete candidate "${candidate.full_name}"? This cannot be undone.`
      );

      if (confirmed) {
        await deleteCandidate();
      }
    } else {
      alert(
        `Action "${e.target.options[e.target.selectedIndex].text}" triggered for ${candidate.full_name}.`
      );
    }

    // Reset select value state back to default
    setActionValue('');
  };

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    // Status change endpoint not yet implemented in this sprint
    const newClass = getStatusClass(e.target.value as CandidateStatus);
    e.target.className = `grid-status-dropdown ${newClass}`;
  };

  return (
    <tr className="candidate-row">
      <td>
        <span className="timestamp-txt">{candidate.date_added}</span>
      </td>
      <td>
        <strong>{candidate.full_name}</strong>
        <div style={{ fontSize: 11.5, color: '#64748b', marginTop: 2 }}>
          {candidate.job_role}
        </div>
      </td>
      <td>{candidate.sub_department}</td>
      <td>
        <span className={`stage-tag ${stageBadgeClass}`}>{candidate.stage}</span>
      </td>
      <td>
        {candidate.resume_file_name ? (
          <span className="resume-tag">&#128196; {candidate.resume_file_name}</span>
        ) : (
          <span style={{ color: '#94a3b8' }}>—</span>
        )}
      </td>
      <td>
        <div className="status-select-wrapper">
          <select
            className={`grid-status-dropdown ${getStatusClass(candidate.status)}`}
            defaultValue={candidate.status}
            onChange={handleStatusChange}
            aria-label={`Status for ${candidate.full_name}`}
          >
            {STATUS_OPTIONS.map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
      </td>
      <td style={{ textAlign: 'right', paddingRight: 24 }}>
        <select
          className="action-dropdown"
          value={actionValue}
          onChange={handleActionChange}
          aria-label={`Actions for ${candidate.full_name}`}
        >
          <option value="" disabled>Manage</option>
          {ACTION_OPTIONS.map(opt => (
            <option
              key={opt.value}
              value={opt.value}
              style={opt.value === 'delete' ? { color: '#dc2626', fontWeight: 700 } : undefined}
            >
              {opt.label}
            </option>
          ))}
        </select>
      </td>
    </tr>
  );
}