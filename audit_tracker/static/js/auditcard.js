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
    const cardbody = document.getElementById("card");

    async function loadTableData() {
        if (!cardbody) return;
        try {
            let response = await fetch("/audit_details");
            let data = await response.json();
            cardbody.innerHTML = "";

            if (!Array.isArray(data) || data.length === 0) {
                cardbody.innerHTML = `<div class="col-span-full text-center py-12 text-gray-400 bg-gray-900 rounded-xl border border-gray-800"><i class="fas fa-folder-open text-4xl text-yellow-500 mb-3 block"></i>No open audit opportunities available at this time.</div>`;
                return;
            }

            data.forEach((item) => {
                let card = document.createElement("div");
                card.className = "bg-gray-900 border border-gray-800 hover:border-yellow-500 rounded-xl p-6 shadow-xl transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between";

                card.innerHTML = `
                    <div>
                        <div class="flex justify-between items-start mb-4">
                            <span class="bg-yellow-500/10 text-yellow-400 border border-yellow-500/30 px-3 py-1 rounded-full text-xs font-bold font-mono">${item.Audit_id}</span>
                            <span class="bg-green-900/40 text-green-400 border border-green-500/30 px-3 py-1 rounded-full text-xs font-bold">₹${item.Amount} / Audit</span>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-2">${item.Audit_type || 'General Financial Audit'}</h3>
                        <p class="text-gray-400 text-sm mb-4"><i class="fas fa-building text-yellow-500 mr-2"></i><span class="font-semibold text-gray-300">Industry:</span> ${item.industry || 'N/A'}</p>
                        
                        <div class="grid grid-cols-2 gap-3 text-xs text-gray-300 mb-6 bg-gray-950 p-4 rounded-lg border border-gray-800">
                            <div><i class="fas fa-calendar-alt text-yellow-500 mr-1.5"></i><span class="text-gray-400">Date:</span> ${item.Date}</div>
                            <div><i class="fas fa-clock text-yellow-500 mr-1.5"></i><span class="text-gray-400">Duration:</span> ${item.Days} Day(s)</div>
                            <div><i class="fas fa-user-friends text-yellow-500 mr-1.5"></i><span class="text-gray-400">Needed:</span> ${item.Auditors_require} Auditor(s)</div>
                            <div><i class="fas fa-graduation-cap text-yellow-500 mr-1.5"></i><span class="text-gray-400">Req:</span> ${item.Qualification || 'Graduate'}</div>
                            <div><i class="fas fa-laptop text-yellow-500 mr-1.5"></i><span class="text-gray-400">Equip:</span> ${item.equipment || 'Laptop Required'}</div>
                            <div><i class="fas fa-map-marker-alt text-red-400 mr-1.5"></i><span class="text-gray-400">Loc:</span> ${item.loction || item.state}</div>
                        </div>
                    </div>

                    <button class="apply-btn w-full bg-yellow-500 hover:bg-yellow-400 text-black font-bold py-2.5 px-4 rounded-lg transition-colors flex items-center justify-center gap-2">
                        <span>Apply Now</span>
                        <i class="fas fa-arrow-right"></i>
                    </button>
                `;

                const applyBtn = card.querySelector('.apply-btn');
                if (applyBtn) {
                    applyBtn.addEventListener("click", async function () {
                        const payload = {
                            audit_id: item.Audit_id,
                            whatsappLink: item.whatsappLink
                        };
                        try {
                            let res = await fetch('/apply/user_Details', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ data: payload })
                            });

                            if (res.ok) {
                                showToast("Selected audit. Redirecting to registration...", false);
                                setTimeout(() => {
                                    window.location.href = '/apply/user_Details';
                                }, 800);
                            } else {
                                showToast("Failed to process audit application request.", true);
                            }
                        } catch (err) {
                            console.error("Apply click error:", err);
                            showToast("Connection error while processing application.", true);
                        }
                    });
                }

                cardbody.appendChild(card);
            });
        } catch (error) {
            console.error("Error loading cards:", error);
            showToast("Failed to load available audit opportunities.", true);
        }
    }

    loadTableData();
});
