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

document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById('submit');
    if (!submitBtn) return;

    submitBtn.addEventListener("click", async () => {
        const elements = document.querySelectorAll('.input');
        let data = {};

        elements.forEach((ele) => {
            if (ele.name) {
                let name = ele.name.trim();
                let value = ele.value ? ele.value.trim() : '';
                data[name] = value;
            }
        });

        if (!data['Audit Id'] || !data['Auditor type']) {
            showToast("Please fill in Audit Id and Audit Type.", true);
            return;
        }

        try {
            let response = await fetch("/admin/manual_update", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "data": data })
            });

            let msg = await response.json();

            if (response.ok) {
                showToast(typeof msg === 'string' ? msg : "Audit added successfully!", false);
                setTimeout(() => {
                    window.location.href = '/admin/dashboard';
                }, 1000);
            } else {
                showToast(msg.error || "Failed to save audit data.", true);
            }
        } catch (error) {
            console.error("Error submitting manual audit:", error);
            showToast("An error occurred while saving data.", true);
        }
    });
});
