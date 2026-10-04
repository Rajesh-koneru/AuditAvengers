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

async function register(e) {
    if (e) e.preventDefault();
    let nameEl = document.getElementById('name');
    let mailEl = document.getElementById('email');
    let phoneEl = document.getElementById('phone');

    let name = nameEl ? nameEl.value.trim() : '';
    let mail = mailEl ? mailEl.value.trim() : '';
    let phone = phoneEl ? phoneEl.value.trim() : '';

    if (!name || !mail || !phone) {
        showToast("Please enter your Name, Email, and Phone number.", true);
        return;
    }

    try {
        let response = await fetch('/apply/audit_application', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, email: mail, phone: phone })
        });

        let data = await response.json();
        if (response.ok) {
            showToast(data['message'] || "Registration successful!", false);
            setTimeout(() => {
                if (data['link']) {
                    window.location.href = data['link'];
                } else {
                    window.location.href = '/';
                }
            }, 1200);
        } else {
            showToast(data['error'] || "Registration failed.", true);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        showToast('Failed to connect to registration service.', true);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById('button');
    if (btn) {
        btn.addEventListener('click', register);
    }
});
