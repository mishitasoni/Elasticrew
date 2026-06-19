import type { Candidate } from '../../types/candidate';
import { CandidateRow } from './CandidateRow';

interface CandidateTableProps {
  candidates: Candidate[];
  loading: boolean;
}

function SkeletonRow() {
  const shimmer: React.CSSProperties = {
    background: 'linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%)',
    backgroundSize: '200% 100%',
    animation: 'shimmer 1.4s infinite',
    borderRadius: 6,
    height: 16,
    display: 'inline-block',
    width: '100%',
  };
  return (
    <tr>
      {[80, 160, 100, 150, 120, 90, 80].map((w, i) => (
        <td key={i}>
          <span style={{ ...shimmer, width: w }} />
        </td>
      ))}
    </tr>
  );
}

export function CandidateTable({ candidates, loading }: CandidateTableProps) {
  return (
    <div className="candidates-section">
      <style>{`
        @keyframes shimmer {
          0%   { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>
      <div className="table-responsive-wrapper">
        <table className="candidate-table" aria-label="Candidates list">
          <thead>
            <tr>
              <th>Date Added</th>
              <th>Candidate Name</th>
              <th>Sub Dept</th>
              <th>Pipeline Stage</th>
              <th>ElastiCrew Resume</th>
              <th>Admin Status</th>
              <th style={{ textAlign: 'right', paddingRight: 24 }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <>
                <SkeletonRow />
                <SkeletonRow />
                <SkeletonRow />
              </>
            ) : candidates.length === 0 ? (
              <tr>
                <td colSpan={7}>
                  <div className="empty-state">
                    No candidates found in this view context.
                  </div>
                </td>
              </tr>
            ) : (
              candidates.map(c => <CandidateRow key={c.id} candidate={c} />)
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
