document.addEventListener("DOMContentLoaded", function () {
    const totalEl = document.getElementById('totalAudits');
    const activeEl = document.getElementById('active_audits');
    const completeEl = document.getElementById('complete_audits');
    const pendingEl = document.getElementById('pending');
    const tableBody = document.getElementById('table_body');
    const progressFill = document.getElementById('completionProgressFill');
    const progressText = document.getElementById('completionProgressText');

    async function loadDashboardMetrics() {
        try {
            const [totalRes, activeRes, completeRes, pendingRes] = await Promise.all([
                fetch("/admin/total_audits"),
                fetch("/admin/active_audits"),
                fetch("/admin/complete"),
                fetch("/admin/pending")
            ]);

            const total = await totalRes.json();
            const active = await activeRes.json();
            const complete = await completeRes.json();
            const pending = await pendingRes.json();

            if (totalEl) totalEl.innerText = total || 0;
            if (activeEl) activeEl.innerText = active || 0;
            if (completeEl) completeEl.innerText = complete || 0;
            if (pendingEl) pendingEl.innerText = pending || 0;

            if (progressFill && progressText) {
                const totalNum = Number(total) || 0;
                const completeNum = Number(complete) || 0;
                const rate = totalNum > 0 ? Math.round((completeNum / totalNum) * 100) : 0;
                progressFill.style.width = `${rate}%`;
                progressText.innerText = `${rate}% Audit Completion Rate (${completeNum}/${totalNum})`;
            }
        } catch (err) {
            console.error("Error loading metrics:", err);
        }
    }

    async function loadRecentAudits() {
        try {
            let response = await fetch("/admin/Recent_audit");
            let data = await response.json();

            if (!tableBody) return;
            tableBody.innerHTML = "";

            if (!Array.isArray(data) || data.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-gray-500">No recent audits found.</td></tr>`;
                return;
            }

            data.forEach((val) => {
                let row = document.createElement('tr');
                row.className = "border-b border-gray-800 hover:bg-gray-800 transition-colors";
                const statusBadge = val.audit_status === 'Completed' 
                    ? '<span class="bg-green-900 text-green-300 px-2 py-0.5 rounded-full text-xs font-semibold border border-green-500">Completed</span>'
                    : val.audit_status === 'In Progress' 
                    ? '<span class="bg-blue-900 text-blue-300 px-2 py-0.5 rounded-full text-xs font-semibold border border-blue-500">In Progress</span>'
                    : '<span class="bg-amber-900 text-amber-300 px-2 py-0.5 rounded-full text-xs font-semibold border border-amber-500">Pending</span>';

                row.innerHTML = `
                    <td class="py-3 px-4 font-mono text-yellow-400 text-sm font-bold">${val.auditor_id || 'N/A'}</td>
                    <td class="py-3 px-4 text-white text-sm font-semibold">${val.auditor_name || 'N/A'}</td>
                    <td class="py-3 px-4 text-gray-300 text-sm">${val.Audit_id || 'N/A'}</td>
                    <td class="py-3 px-4 text-gray-400 text-sm">${val.planned_Date || 'N/A'}</td>
                    <td class="py-3 px-4 text-sm">${statusBadge}</td>
                `;
                tableBody.append(row);
            });
        } catch (err) {
            console.error("Error loading recent audits:", err);
        }
    }

    loadDashboardMetrics();
    loadRecentAudits();
});