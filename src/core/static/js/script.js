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

  // Search bar
  $("#searchBar").on("keyup", function () {
    var query = $(this).val();
    $.ajax({
      url: "",
      data: { q: query },
      dataType: "json",
      success: function (response) {
        // Replace the envoy list with the new HTML
        $(".row").html(response.html);
      },
    });
  });
});
