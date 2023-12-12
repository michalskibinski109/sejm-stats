$(document).ready(function () {
  $(".counter").each(function () {
    var counter = $(this);
    var target = +counter.text();
    counter.text(`${Math.max(target - 20, 0)}`); // adjust this value to set the starting count
    var interval = setInterval(function () {
      var current = +counter.text();
      if (current < target) {
        counter.text(current + 1);
      } else {
        clearInterval(interval);
      }
    }, 20); // adjust this value to change the speed of the animation
  });
});
