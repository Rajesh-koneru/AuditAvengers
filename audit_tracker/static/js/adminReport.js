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
    let isUpdateMode = false;
    const toggleButton = document.getElementById("editBtn");
    const tableBody = document.querySelector(".table_body");
    const searchInput = document.getElementById("search_input");

    let loadedAuditData = [];

    async function loadTableData() {
        try {
            let response = await fetch("/admin/report");
            loadedAuditData = await response.json();
            renderTable(loadedAuditData);
        } catch (error) {
            console.error("Error fetching audit data:", error);
            showToast("Failed to fetch audit report data.", true);
        }
    }

    function renderTable(dataList) {
        if (!tableBody) return;
        tableBody.innerHTML = "";

        if (!Array.isArray(dataList) || dataList.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="13" class="text-center py-6 text-gray-400">No matching audit records found.</td></tr>`;
            return;
        }

        dataList.forEach((item) => {
            let row = document.createElement("tr");
            row.className = 'rowData border-b border-gray-800 hover:bg-gray-800 transition-colors';

            const statusClass = item.audit_status === 'Completed' ? 'bg-green-900 text-green-300 border border-green-500' : item.audit_status === 'In Progress' ? 'bg-amber-900 text-amber-300 border border-amber-500' : 'bg-red-900 text-red-300 border border-red-500';
            const payClass = item.payment_status === 'Paid' ? 'bg-green-900 text-green-300 border border-green-500' : item.payment_status === 'Requested' ? 'bg-blue-900 text-blue-300 border border-blue-500' : 'bg-amber-900 text-amber-300 border border-amber-500';

            row.innerHTML = `
                <td class="bg-gray-900 text-yellow-400 font-bold p-3 text-center">${item.Audit_id}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.auditor_id}</td>
                <td class="bg-gray-900 text-white font-semibold p-3 text-center">${item.auditor_name}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.audit_type}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.planned_date}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.contact}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.email}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.client_id}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.state}</td>
                <td class="bg-gray-900 text-gray-300 p-3 text-center">${item.location}</td>
                <td class="bg-gray-900 text-green-400 font-bold p-3 text-center">₹${item.payment_amount}</td>
                <td class="paymentColor p-3 text-center" data-field="payment_status" ${isUpdateMode ? 'data-id="'+ item.auditor_id + '"' : ''}>
                    <span class="px-2.5 py-1 rounded-full text-xs font-semibold ${payClass}">${item.payment_status}</span>
                </td>
                <td class="StatusColor p-3 text-center" data-field="status" ${isUpdateMode ? 'data-id="' + item.auditor_id + '"' : ''}>
                    <span class="px-2.5 py-1 rounded-full text-xs font-semibold ${statusClass}">${item.audit_status}</span>
                </td>
            `;
            tableBody.appendChild(row);
        });

        if (isUpdateMode) {
            enableEditing();
        }
    }

    // Instant Client-side Search Filter
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = this.value.toLowerCase().trim();
            if (!query) {
                renderTable(loadedAuditData);
                return;
            }
            const filtered = loadedAuditData.filter(item => 
                (item.Audit_id && item.Audit_id.toLowerCase().includes(query)) ||
                (item.auditor_name && item.auditor_name.toLowerCase().includes(query)) ||
                (item.auditor_id && item.auditor_id.toLowerCase().includes(query)) ||
                (item.state && item.state.toLowerCase().includes(query)) ||
                (item.location && item.location.toLowerCase().includes(query)) ||
                (item.email && item.email.toLowerCase().includes(query))
            );
            renderTable(filtered);
        });
    }

    function enableEditing() {
        if (!tableBody) return;
        tableBody.addEventListener("click", function (event) {
            let td = event.target.closest("td");
            if (td && td.hasAttribute("data-field") && !td.querySelector("select")) {
                let auditId = td.getAttribute("data-id");
                let fieldType = td.getAttribute("data-field");
                let currentValue = td.textContent.trim();

                let select = document.createElement("select");
                select.className = "bg-gray-800 text-white text-xs border border-yellow-500 rounded p-1 focus:outline-none";
                let options = fieldType === "status"
                    ? ["Completed", "Pending", "In Progress"]
                    : ["Paid", "Unpaid", "Requested"];

                options.forEach(option => {
                    let opt = document.createElement("option");
                    opt.value = option;
                    opt.textContent = option;
                    if (option === currentValue) opt.selected = true;
                    select.appendChild(opt);
                });

                td.innerHTML = "";
                td.appendChild(select);
                select.focus();

                select.addEventListener("change", async function () {
                    let newStatus = this.value.trim();
                    if (auditId && newStatus) {
                        if (fieldType === "status") {
                            await updateStatus(auditId, newStatus);
                        } else if (fieldType === "payment_status") {
                            await paymentUpdate(auditId, newStatus);
                        }
                    }
                });

                select.addEventListener("blur", function () {
                    loadTableData();
                });
            }
        });
    }

    async function updateStatus(auditId, newStatus) {
        try {
            const response = await fetch("/admin/update_status", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "Id": auditId, "value": newStatus })
            });
            const data = await response.json();
            if (response.ok) {
                showToast(data.message || "Status updated successfully!", false);
                loadTableData();
            } else {
                showToast(data.error || "Failed to update status", true);
            }
        } catch (error) {
            console.error("Error updating status:", error);
            showToast("Network error while updating status", true);
        }
    }

    async function paymentUpdate(auditId, paymentStatus) {
        try {
            const response = await fetch("/admin/update_payment", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "Id": auditId, "value": paymentStatus })
            });
            const data = await response.json();
            if (response.ok) {
                showToast(data.message || "Payment status updated successfully!", false);
                loadTableData();
            } else {
                showToast(data.error || "Failed to update payment", true);
            }
        } catch (error) {
            console.error("Error updating payment status:", error);
            showToast("Network error while updating payment status", true);
        }
    }

    if (toggleButton) {
        toggleButton.addEventListener("click", function () {
            isUpdateMode = !isUpdateMode;
            toggleButton.innerText = isUpdateMode ? "Done Editing" : "Edit Status";
            toggleButton.className = isUpdateMode 
                ? "bg-green-600 text-white px-3 py-2 rounded-lg flex items-center gap-2 hover:bg-green-700 transition"
                : "bg-yellow-500 text-black px-3 py-2 rounded-lg flex items-center gap-2 hover:bg-yellow-400 transition font-semibold";
            showToast(isUpdateMode ? "Click any status pill to edit" : "Edit mode closed", false);
            loadTableData();
        });
    }

    const filterBtn = document.getElementById("filterBtn");
    if (filterBtn) {
        filterBtn.addEventListener("click", async function () {
            let filterVal = document.getElementById('filter').value;
            try {
                const response = await fetch("/admin/filter", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ "data": filterVal })
                });
                const data = await response.json();
                if (response.ok) {
                    renderTable(data);
                    showToast(`Filtered records for: ${filterVal}`, false);
                } else {
                    showToast(data.error || "Filter failed", true);
                }
            } catch (error) {
                console.error("Filter error:", error);
                showToast("Network error during filter", true);
            }
        });
    }

    const uploadButton = document.getElementById('uploadButton');
    if (uploadButton) {
        uploadButton.addEventListener('click', function (event) {
            event.preventDefault();
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];

            if (!file) {
                showToast("Please select an Excel file first!", true);
                return;
            }

            const reader = new FileReader();
            reader.onload = function (event) {
                try {
                    const data = new Uint8Array(event.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const sheetName = workbook.SheetNames[0];
                    const sheet = workbook.Sheets[sheetName];
                    const jsonData = XLSX.utils.sheet_to_json(sheet, { raw: false, dateNF: "yyyy-mm-dd" });

                    if (jsonData.length === 0) {
                        showToast("The selected Excel file is empty.", true);
                        return;
                    }

                    fetch('/upload-excel', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ "data": jsonData })
                    })
                    .then(res => res.json())
                    .then(resData => {
                        if (resData.message) {
                            showToast(resData.message, false);
                            loadTableData();
                        } else {
                            showToast(resData.error || "Upload failed", true);
                        }
                    })
                    .catch(err => {
                        console.error("Upload error:", err);
                        showToast("Error uploading file to server", true);
                    });
                } catch (err) {
                    console.error("Excel parse error:", err);
                    showToast("Error reading Excel file format", true);
                }
            };
            reader.readAsArrayBuffer(file);
        });
    }

    const downloadBtn = document.getElementById('download');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', async () => {
            try {
                const nameInput = document.getElementById('fileName');
                const val = nameInput ? nameInput.value.trim() : 'audit_report';
                const response = await fetch('/admin/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ "fileName": val })
                });

                if (!response.ok) {
                    showToast("Failed to generate report download.", true);
                    return;
                }

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${val || 'audit_report'}.xlsx`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                showToast("Excel report downloaded successfully!", false);
            } catch (error) {
                console.error("Download error:", error);
                showToast("Error downloading file.", true);
            }
        });
    }

    loadTableData();
});
