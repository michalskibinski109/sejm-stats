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
  $(document).ready(function () {
    // Counter and other unrelated logic omitted for brevity

    $.ajax({
      url: "/last-update/", // Adjust the URL to your actual endpoint
      success: function (response) {
        var message = response.last_updated
          ? `Server was last updated on: ${response.last_updated}`
          : response.message;

        // Toast HTML structure adjusted for proper nesting
        var toastHTML = `
          <div class="m-2 toast align-items-center text-white bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
              <div class="toast-body">
                ${message}
              </div>
              <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
          </div>
        `;

        $("#toastContainer").append(toastHTML);
        var toastElement = $(".toast").last(); // Target the last toast appended
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
      },
      error: function () {
        // Similar structure for error handling
        var toastHTML = `
          <div class="m-2 toast align-items-center text-white bg-warning border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
              <div class="toast-body">
                Failed to fetch last update time.
              </div>
              <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
          </div>
        `;

        $("#toastContainer").append(toastHTML);
        var toastElement = $(".toast").last(); // Target the last toast appended
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
      },
    });

    // Initial static toast for "Wspomóż mnie"
    var initialToastHTML = `
      <div class="m-2  toast align-items-center text-white bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body fw-bold">
            Wspomóż mnie na <a href="https://patronite.pl/sejm-stats" class="text-white">Patronite</a>
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    `;
    // Append and show the initial toast
    $("#toastContainer").append(initialToastHTML);
    var initialToastElement = $(".toast").last();
    var initialToast = new bootstrap.Toast(initialToastElement);
    initialToast.show();
  });
});
