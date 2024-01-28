$(document).ready(function () {
  var ctx = $("#envoysChart").get(0).getContext("2d");
  let clubs_str = $("#envoysChart").attr("data-clubs");
  // parse it to string
  var clubs = JSON.parse(clubs_str);
  var labels = clubs.map(function (club) {
    return club.id;
  });
  var data = clubs.map(function (club) {
    return club.envoys_count;
  });

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Number of Envoys",
          data: data,

          hoverOffset: 4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Club Envoys Distribution",
        },
      },
    },
  });
});
