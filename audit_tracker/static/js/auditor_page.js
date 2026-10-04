function showToast(message, isError = false) {
    let toast = document.getElementById("custom-toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "custom-toast";
        toast.className = "fixed bottom-5 right-5 z-50 px-6 py-3 rounded-lg shadow-xl text-white text-sm font-semibold transition-all duration-300 opacity-0 transform translate-y-2";
        document.body.appendChild(toast);
    }
    toast.className = `fixed bottom-5 right-5 z-50 px-6 py-3 rounded-lg shadow-xl text-white text-sm font-semibold transition-all duration-300 transform translate-y-0 ${isError ? 'bg-red-600' : 'bg-green-600'}`;
    toast.innerText = message;
    toast.style.opacity = "1";
    setTimeout(() => {
        toast.style.opacity = "0";
    }, 3500);
}

document.addEventListener("DOMContentLoaded", async function() {
    let nameEl = document.getElementById('name');
    let tableBody = document.querySelector('.tbody');
    let auditorName = "";
    let auditorId = "";

    try {
        let response = await fetch("/auditor/auditor_details");
        let data = await response.json();

        if (data.username) {
            auditorName = data.username;
            auditorId = data.id;
            if (nameEl) nameEl.innerText = auditorName;
        }

        async function fetchData() {
            try {
                let res = await fetch("/auditor/data", {
                    method: 'POST',
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ "Id": auditorId, 'username': auditorName })
                });

                if (!res.ok) throw new Error(`HTTP error ${res.status}`);

                let auditList = await res.json();
                if (tableBody) tableBody.innerHTML = "";

                if (Array.isArray(auditList) && auditList.length > 0) {
                    auditList.forEach((item) => {
                        let row = document.createElement("tr");
                        row.className = "border-b border-gray-800 hover:bg-gray-800 transition-colors";
                        row.innerHTML = `
                            <td class="bg-gray-900 text-yellow-400 font-bold p-3 text-center">${item.Audit_id}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.auditor_id}</td>
                            <td class="bg-gray-900 text-white p-3 text-center">${item.auditor_name}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.audit_type}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.planned_date}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.contact}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.email}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.client_id}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.state}</td>
                            <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.location}</td>
                            <td class="bg-gray-900 text-green-400 font-semibold p-3 text-center">₹${item.payment_amount}</td>
                            <td class="bg-gray-900 p-3 text-center">
                                <span class="px-2.5 py-1 rounded-full text-xs font-semibold ${item.payment_status === 'Paid' ? 'bg-green-900 text-green-300 border border-green-500' : 'bg-yellow-900 text-yellow-300 border border-yellow-500'}">${item.payment_status}</span>
                            </td>
                            <td class="bg-gray-900 p-3 text-center">
                                <span class="px-2.5 py-1 rounded-full text-xs font-semibold ${item.audit_status === 'Completed' ? 'bg-green-900 text-green-300 border border-green-500' : item.audit_status === 'In Progress' ? 'bg-blue-900 text-blue-300 border border-blue-500' : 'bg-amber-900 text-amber-300 border border-amber-500'}">${item.audit_status}</span>
                            </td>
                        `;
                        if (tableBody) tableBody.appendChild(row);
                    });
                } else if (tableBody) {
                    tableBody.innerHTML = `<tr><td colspan="13" class="text-center py-6 text-gray-400">No active audit assignments found for your account.</td></tr>`;
                }
            } catch (err) {
                console.error("Error fetching auditor data:", err);
            }
        }
        fetchData();

    } catch (err) {
        console.error("Error fetching auditor details:", err);
    }

    const btn = document.getElementById('btnStatus');
    if (btn) {
        btn.addEventListener('click', async () => {
            const selectEl = document.getElementById('update');
            const newStatus = selectEl ? selectEl.value : 'Completed';

            try {
                let res = await fetch("/auditor/status_update", {
                    method: 'POST',
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ "status": newStatus, "id": auditorId || auditorName })
                });

                let data = await res.json();
                if (res.ok) {
                    showToast(data.message || "Audit status updated successfully!", false);
                    setTimeout(() => location.reload(), 1200);
                } else {
                    showToast(data.error || "Failed to update status", true);
                }
            } catch (e) {
                console.error("Update error:", e);
                showToast("Failed to connect to server.", true);
            }
        });
    }
});