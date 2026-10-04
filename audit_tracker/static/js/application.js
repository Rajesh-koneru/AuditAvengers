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

document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector(".table_body");
    const searchInput = document.getElementById("search_input");
    let loadedApplications = [];

    async function loadTableData() {
        try {
            let response = await fetch("/admin/application");
            loadedApplications = await response.json();
            renderTable(loadedApplications);
        } catch (error) {
            console.error("Error fetching application data:", error);
            showToast("Failed to fetch applications", true);
        }
    }

    function renderTable(dataList) {
        if (!tableBody) return;
        tableBody.innerHTML = "";

        if (!Array.isArray(dataList) || dataList.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="12" class="text-center py-6 text-gray-400">No applicant records found.</td></tr>`;
            return;
        }

        dataList.forEach((item) => {
            let row = document.createElement("tr");
            row.className = 'rowData border-b border-gray-800 hover:bg-gray-800 transition-colors';
            row.innerHTML = `
                <td class="bg-gray-900 text-yellow-400 font-bold p-3 text-center">${item.Audit_id}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.Auditor_id}</td>
                <td class="bg-gray-900 text-white font-semibold p-3 text-center">${item.Auditor_name}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.audit_type}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.Date}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.phone}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.email}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.state}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.Client_id}</td>
                <td class="bg-gray-900 p-3 text-center">
                  <input
                    type="number"
                    placeholder="Compensation (₹)"
                    value="1000"
                    class="bg-gray-800 border border-gray-700 text-green-400 px-3 py-1 rounded w-32 focus:outline-none focus:border-yellow-500 text-center font-bold"
                  />
                </td>
                <td class="bg-gray-900 p-3 text-center">
                    <button
                      class="toggle-btn px-3 py-1 rounded text-xs font-bold transition-all ${item.status === 'accepted' ? 'bg-green-600 text-white hover:bg-green-700' : 'bg-red-600 text-white hover:bg-red-700'}"
                      data-auditor-id="${item.Auditor_id}"
                    >
                      ${item.status === 'accepted' ? 'Accepted' : 'Rejected'}
                    </button>
                </td>
                <td class="bg-gray-900 p-3 text-center">
                    <button class="submitBtn bg-yellow-500 text-black px-3 py-1.5 rounded-lg text-xs font-bold flex items-center justify-center gap-1 hover:bg-yellow-400 transition mx-auto">
                        <i class="fas fa-check-circle"></i> Approve & Assign
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });

        attachRowEvents();
    }

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.toLowerCase().trim();
            if (!query) {
                renderTable(loadedApplications);
                return;
            }
            const filtered = loadedApplications.filter(item =>
                (item.Audit_id && item.Audit_id.toLowerCase().includes(query)) ||
                (item.Auditor_name && item.Auditor_name.toLowerCase().includes(query)) ||
                (item.Auditor_id && item.Auditor_id.toLowerCase().includes(query)) ||
                (item.phone && item.phone.toLowerCase().includes(query)) ||
                (item.state && item.state.toLowerCase().includes(query))
            );
            renderTable(filtered);
        });
    }

    function attachRowEvents() {
        document.querySelectorAll('.toggle-btn').forEach(button => {
            button.addEventListener('click', async function () {
                const auditId = this.dataset.auditorId;
                const newStatus = this.textContent.trim() === 'Accepted' ? 'rejected' : 'accepted';

                try {
                    const response = await fetch(`/applications/status`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ status: newStatus, Id: auditId })
                    });

                    if (response.ok) {
                        this.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);
                        if (newStatus === 'accepted') {
                            this.className = 'toggle-btn px-3 py-1 rounded text-xs font-bold transition-all bg-green-600 text-white hover:bg-green-700';
                        } else {
                            this.className = 'toggle-btn px-3 py-1 rounded text-xs font-bold transition-all bg-red-600 text-white hover:bg-red-700';
                        }
                        showToast(`Application status set to ${newStatus}`, false);
                    } else {
                        showToast('Failed to update application status', true);
                    }
                } catch (err) {
                    console.error("Error updating status:", err);
                    showToast("Error connecting to server", true);
                }
            });
        });

        document.querySelectorAll('.submitBtn').forEach((button) => {
            button.addEventListener('click', async function () {
                const tr = this.closest('tr');
                if (!tr) return;

                const cells = tr.getElementsByTagName("td");
                const statusButton = cells[10].querySelector('button');
                const paymentInput = cells[9].querySelector('input');

                const status = statusButton ? statusButton.textContent.trim() : 'Accepted';
                const paymentVal = paymentInput ? paymentInput.value.trim() : '1000';

                const sendData = [{
                    audit_id: cells[0]?.innerText.trim(),
                    auditor_id: cells[1]?.innerText.trim(),
                    auditor_name: cells[2]?.innerText.trim(),
                    audit_type: cells[3]?.innerText.trim(),
                    Date: cells[4]?.innerText.trim(),
                    phone: cells[5]?.innerText.trim(),
                    email: cells[6]?.innerText.trim(),
                    state: cells[7]?.innerText.trim(),
                    client_id: cells[8]?.innerText.trim(),
                    payment: paymentVal,
                    status: status
                }];

                try {
                    const response = await fetch("/application/audit_report", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(sendData)
                    });
                    const result = await response.json();

                    if (response.ok) {
                        showToast(result['message'] || "Application promoted to Audit Report!", false);

                        const phoneNumber = result['phone'] || sendData[0].phone;
                        const name = result['auditor_name'] || sendData[0].auditor_name;
                        const password = result['auditor_id'] || sendData[0].auditor_id;
                        const message = `Hello ${name}! Congratulations, your auditor application has been APPROVED for Audit Avengers. Your login ID: ${password}`;
                        const whatsappURL = `https://wa.me/+91${phoneNumber}?text=${encodeURIComponent(message)}`;

                        window.open(whatsappURL, '_blank');
                        setTimeout(() => loadTableData(), 1000);
                    } else {
                        showToast(result.error || "Failed to assign auditor", true);
                    }
                } catch (error) {
                    console.error("Error submitting row:", error);
                    showToast("Error connecting to server", true);
                }
            });
        });
    }

    loadTableData();
});
