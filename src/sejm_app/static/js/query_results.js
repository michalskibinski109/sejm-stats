$(document).ready(function () {
  $.ajax({
    url: "/api/search/", // Replace with the URL of your API view
    data: {
      search: "your search query", // Replace with your search query
    },
    dataType: "json",
    success: function (data) {
      // Update the page with the data
      // For example:
      //   $(".counter").text(data.total);
      // Add more code here to update other parts of the page
    },
  });
  console.log("🚀 ~ data:", data);
});
