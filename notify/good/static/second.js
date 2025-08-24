document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".msg");

    const actionDelays = {
        like_photo: 4000,
        transaction: 1000,
        login: 2000,
        logout: 4000
        
    };

    // Helper function to get CSRF token from cookie
    function getCSRFToken() {
        const name = "csrftoken";
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return null;
    }

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const action = btn.dataset.action;
            const delay = actionDelays[action] || 1000;

            btn.innerText = "Sending...";

            setTimeout(() => {
                fetch(sendNotificationUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body: `action=${encodeURIComponent(action)}`
                })
                .then(res => res.json())
                .then(data => {
                    btn.innerText = data.status === "success" ? "Sent!" : "Failed!";
                    console.log("Action sent:", data.action);
                })
                .catch(err => {
                    console.error("Fetch error:", err);
                    btn.innerText = "Error!";
                });
            }, delay);
        });
    });
});