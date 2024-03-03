$(document).ready(function () {
  // Extract data from the 'data-interpolations' attribute
  var data = $("#disciplineChart").data("discipline");
  //   data = JSON.parse(data);
  var names = Object.keys(data);
  var values = Object.values(data);
  // Create the chart
  console.log(data);
  var ctx = $("#disciplineChart").get(0).getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: names,
      datasets: [
        {
          data: values,
        },
      ],
    },
    options: {
      tension: 0.2,
      maintainAspectRatio: false,
      aspectRatio: 0.7,
      responsive: true,
      plugins: {
        // legend: {
        //   position: "top",
        // },
      },
    },
  });
});
