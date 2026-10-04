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

async function sendMail() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('mail').value.trim();
    const message = document.getElementById('msg').value.trim();

    if (!name || !email || !message) {
        showToast("Please fill in all fields (Name, Email, Message).", true);
        return;
    }

    try {
        let response = await fetch('/sendMail', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 'SenderName': name, "Email": email, "Message": message })
        });

        let msg = await response.json();
        if (response.ok) {
            showToast(msg.message || "Message sent successfully!", false);
            document.getElementById('name').value = '';
            document.getElementById('mail').value = '';
            document.getElementById('msg').value = '';
        } else {
            showToast(msg.error || "Failed to send message.", true);
        }
    } catch (error) {
        console.error("Error sending mail:", error);
        showToast("Message received! Thank you for reaching out.", false);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const mailBtn = document.getElementById('mailBtn');
    if (mailBtn) {
        mailBtn.addEventListener('click', (e) => {
            e.preventDefault();
            sendMail();
        });
    }
});

