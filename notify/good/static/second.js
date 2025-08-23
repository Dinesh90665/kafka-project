document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".msg");

    // Define delay for each action in milliseconds
    const actionDelays = {
        like_photo: 1000,       // 1 second
        transaction: 2000,      // 2 seconds
        login: 3000,            // 3 seconds
        logout: 4000,           // 4 seconds
        post_photo: 1500,       // example
        added_item: 2500,
        login_system: 3500
    };

    buttons.forEach(btn => {
        btn.onclick = () => {
            const action = btn.dataset.action;
            const delay = actionDelays[action] || 1000;

            btn.innerText = "Sending...";

            setTimeout(() => {
                // Example fetch call (adjust URL if needed)
                fetch("/send_notification/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body: `action=${action}`
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "success") {
                        btn.innerText = "Sent!";
                    } else {
                        btn.innerText = "Failed!";
                    }
                });
            }, delay);
        };
    });

    // Helper function to get CSRF token from cookie
    function getCSRFToken() {
        let cookieValue = null;
        const name = "csrftoken";
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
