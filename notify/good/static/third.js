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

  document.getElementById("preferences-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch(savePreferenceUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken()
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      const resultBox = document.getElementById("result");
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
      const resultBox = document.getElementById("result");
      resultBox.textContent = "An error occurred.";
      resultBox.className = "error";
    });
  });