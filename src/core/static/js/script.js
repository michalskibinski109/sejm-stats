document.getElementById("theme-toggle").addEventListener("click", function () {
  var html = document.querySelector("html");
  var theme = html.getAttribute("data-bs-theme");
  html.setAttribute("data-bs-theme", theme === "dark" ? "light" : "dark");
});

$(document).ready(function () {
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
