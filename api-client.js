/**
 * api-client.js
 * Frontend API client — thin wrapper around fetch() for all ElastiCrew API calls.
 * Include this file in any HTML page that needs live backend data.
 *
 * Usage:
 *   <script src="api-client.js"></script>
 *   const { pendingQueue, reviewQueue, stats } = await ElastiCrewAPI.getResumeQueue();
 *
 * BASE_URL auto-detects:
 *   - In the browser it uses the current origin (works when served via Express).
 *   - Override by setting window.ELASTICREW_API_BASE before loading this file.
 *   - In Node.js (tests) falls back to http://localhost:3000/api.
 */

(function (global) {
  'use strict';

  // Allow override before script load: <script>window.ELASTICREW_API_BASE = '...'</script>
  const BASE_URL =
    (typeof global.ELASTICREW_API_BASE === 'string' && global.ELASTICREW_API_BASE) ||
    (typeof window !== 'undefined' ? window.location.origin + '/api' : 'http://localhost:3000/api');

  /**
   * Internal fetch wrapper — normalises JSON responses and throws on errors.
   * @param {string} path   - API path, e.g. '/resume-queue'
   * @param {object} [opts] - fetch init options
   * @returns {Promise<object>} - parsed response body (success guaranteed)
   */
  async function request(path, opts = {}) {
    const url = BASE_URL + path;
    const res  = await fetch(url, {
      ...opts,
      headers: {
        'Content-Type': 'application/json',
        ...(opts.headers || {}),
      },
    });

    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error(`Non-JSON response from ${url} (${res.status})`);
    }

    if (!res.ok || !data.success) {
      throw new Error(data.error || `Request failed with status ${res.status}`);
    }
    return data;
  }

  // ── PUBLIC API ──────────────────────────────────────────────────────────────

  const ElastiCrewAPI = {

    // ── Resume Queue ─────────────────────────────────────────────────────────

    /**
     * Fetch the full resume queue — pending queue, review queue, and KPI stats.
     * @returns {Promise<{stats, pendingQueue, reviewQueue}>}
     */
    getResumeQueue() {
      return request('/resume-queue');
    },

    /**
     * Fetch only the KPI counts (no candidate payloads — fast poll).
     * @returns {Promise<{stats}>}
     */
    getQueueStats() {
      return request('/resume-queue/stats');
    },

    /**
     * Fetch a single anonymized candidate from the queue.
     * @param {string} id  - e.g. 'C-1021'
     * @returns {Promise<{candidate}>}
     */
    getCandidate(id) {
      return request(`/resume-queue/${encodeURIComponent(id)}`);
    },

    /**
     * Update the resume queue status for a candidate.
     * @param {string} id
     * @param {string} status - one of the RESUME_STATUSES values
     * @returns {Promise<{candidate}>}
     */
    updateStatus(id, status) {
      return request(`/resume-queue/${encodeURIComponent(id)}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status }),
      });
    },

    /**
     * Save (overwrite) HR notes for a candidate.
     * @param {string} id
     * @param {string} notes
     * @returns {Promise<{id, hrNotes}>}
     */
    saveNotes(id, notes) {
      return request(`/resume-queue/${encodeURIComponent(id)}/notes`, {
        method: 'PATCH',
        body: JSON.stringify({ notes }),
      });
    },

    /**
     * Add a review comment to a candidate's record.
     * @param {string} id
     * @param {'screening'|'interview'} type
     * @param {string} reviewer
     * @param {string} comment
     * @returns {Promise<{review}>}
     */
    addReview(id, type, reviewer, comment) {
      return request(`/resume-queue/${encodeURIComponent(id)}/reviews`, {
        method: 'POST',
        body: JSON.stringify({ type, reviewer, comment }),
      });
    },

    /**
     * Delete a review entry by its UUID.
     * @param {string} id        - candidate ID
     * @param {string} reviewId  - review UUID
     * @returns {Promise<{id, removedFrom}>}
     */
    removeReview(id, reviewId) {
      return request(
        `/resume-queue/${encodeURIComponent(id)}/reviews/${encodeURIComponent(reviewId)}`,
        { method: 'DELETE' }
      );
    },

    /**
     * Mark a candidate as Withdrawn (convenience shortcut).
     * @param {string} id
     * @returns {Promise<{candidate}>}
     */
    withdrawCandidate(id) {
      return request(`/resume-queue/${encodeURIComponent(id)}/withdraw`, {
        method: 'PATCH',
      });
    },

    // ── Resume View ──────────────────────────────────────────────────────────

    /**
     * Fetch all anonymized resumes (powers the view-resume switcher).
     * @returns {Promise<{candidates}>}
     */
    getAllResumes() {
      return request('/resumes');
    },

    /**
     * Fetch a single anonymized resume.
     * @param {string} id
     * @returns {Promise<{candidate}>}
     */
    getResume(id) {
      return request(`/resumes/${encodeURIComponent(id)}`);
    },

    // ── Meta ─────────────────────────────────────────────────────────────────

    /**
     * Fetch all valid resume statuses and pipeline stage labels.
     * @returns {Promise<{resumeStatuses, pipelineStages}>}
     */
    getStatuses() {
      return request('/statuses');
    },
  };

  // Expose globally and as CommonJS module (for Node.js tests)
  global.ElastiCrewAPI = ElastiCrewAPI;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = ElastiCrewAPI;
  }

})(typeof window !== 'undefined' ? window : global);
