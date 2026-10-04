document.addEventListener("DOMContentLoaded", () => {

    async function checkUserStatus() {
        const getBtn = document.getElementById("get");
        if (!getBtn) return;

        try {
            const response = await fetch("/user/home_page", {
                method: 'GET',
                credentials: 'include'
            });
            let data = await response.json();
            let status = data['status'];
            let role = data['role'];
            let username = data['username'] || '';

            if (status === 'logged_in') {
                getBtn.innerText = 'Dashboard';
                if (role === 'admin') {
                    getBtn.setAttribute('href', '/admin/dashboard');
                } else if (role === 'auditor') {
                    getBtn.setAttribute('href', `/auditor_page/${username}`);
                } else {
                    getBtn.setAttribute('href', '/admin/dashboard');
                }
            } else {
                getBtn.innerText = 'Get Started';
                getBtn.setAttribute('href', '/signup_page');
            }
        } catch (error) {
            console.error("Error checking user session status:", error);
            if (getBtn) {
                getBtn.innerText = 'Get Started';
                getBtn.setAttribute('href', '/signup_page');
            }
        }
    }

    async function loadHomeAuditCards() {
        const cardbody = document.getElementById("card");
        if (!cardbody) return;

        try {
            let response = await fetch("/audit_details");
            let data = await response.json();
            cardbody.innerHTML = "";

            if (!Array.isArray(data) || data.length === 0) {
                cardbody.innerHTML = `<div class="col-span-full text-center py-8 text-gray-400">No active audits listed.</div>`;
                return;
            }

            // Display top 3 open audit cards on homepage
            data.slice(0, 3).forEach((item) => {
                let div = document.createElement("div");
                div.className = "bg-gray-900 border border-gray-800 hover:border-yellow-500 rounded-xl p-6 shadow-xl transition-all duration-300 flex flex-col justify-between m-3";

                div.innerHTML = `
                    <div>
                        <div class="flex justify-between items-center mb-3">
                            <span class="bg-yellow-500/10 text-yellow-400 border border-yellow-500/30 px-3 py-1 rounded-full text-xs font-mono font-bold">${item.Audit_id}</span>
                            <span class="bg-green-900/40 text-green-400 border border-green-500/30 px-3 py-1 rounded-full text-xs font-bold">₹${item.Amount}</span>
                        </div>
                        <h3 class="text-lg font-bold text-white mb-1">${item.Audit_type || 'Audit Task'}</h3>
                        <p class="text-xs text-gray-400 mb-3"><i class="fas fa-industry text-yellow-500 mr-1"></i>${item.industry || 'Financial Services'}</p>
                        <div class="space-y-1 text-xs text-gray-300 mb-4 bg-gray-950 p-3 rounded-lg border border-gray-800">
                            <div><i class="fas fa-calendar-alt text-yellow-500 mr-1.5"></i>Date: ${item.Date}</div>
                            <div><i class="fas fa-map-marker-alt text-red-400 mr-1.5"></i>Location: ${item.loction || item.state}</div>
                            <div><i class="fas fa-clock text-yellow-500 mr-1.5"></i>Days: ${item.Days} Day(s)</div>
                        </div>
                    </div>
                    <button class="apply-btn w-full bg-yellow-500 hover:bg-yellow-400 text-black font-bold py-2 px-3 rounded-lg text-sm transition-colors flex items-center justify-center gap-2">
                        <span>Apply Now</span>
                        <i class="fas fa-arrow-right"></i>
                    </button>
                `;

                const btn = div.querySelector('.apply-btn');
                if (btn) {
                    btn.addEventListener("click", async () => {
                        const payload = { audit_id: item.Audit_id, whatsappLink: item.whatsappLink };
                        try {
                            await fetch('/apply/user_Details', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ data: payload })
                            });
                            window.location.href = '/apply/user_Details';
                        } catch (err) {
                            window.location.href = '/signup_page';
                        }
                    });
                }
                cardbody.appendChild(div);
            });
        } catch (error) {
            console.error("Error loading homepage cards:", error);
        }
    }

    checkUserStatus();
    loadHomeAuditCards();
});