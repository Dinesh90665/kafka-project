document.getElementById("preferences-form").addEventListener("submit", function(e) {
    e.preventDefault();
    let formData = new FormData(this);

    fetch("{% url 'save_preference' %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: formData
    })
    .then(response => response.json()) // now response will be JSON
    .then(data => {
        let resultBox = document.getElementById("result");
        if (data.status === "success") {
            resultBox.textContent = "Preference saved!";
            resultBox.className = "success";
        } else {
            resultBox.textContent = "Failed to save.";
            resultBox.className = "error";
        }
    })
    .catch(err => {
        console.error("Fetch error:", err);
    });
});

// CSRF token helper
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
