// Set theme immediately when the script is loaded
var theme = localStorage.getItem("theme");
if (theme) {
  $("html").attr("data-bs-theme", theme);
}

$(document).ready(function () {
  // Theme toggle
  $("#theme-toggle").click(function () {
    var theme = $("html").attr("data-bs-theme");
    let icon = $("#theme-toggle-icon");
    var newTheme = theme === "dark" ? "light" : "dark";
    $("html").attr("data-bs-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  });
  $("#updateButton").click(function () {
    var url = $("#updateButton").data("href");
    var csrfToken = $("#updateButton").data("csrf");
    $.ajax({
      url: url,
      type: "GET",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      success: function (response) {
        showNotification(response.message);
      },
      error: function (xhr, status, error) {
        showNotification("Update failed: " + error);
      },
    });
  });
});

// Function to show notification
function showNotification(message) {
  // This example uses a simple alert, but you can replace this with any notification mechanism
  alert(message);
}
