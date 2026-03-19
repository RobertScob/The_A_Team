$(document).on("click", "a", function (e) {

     let link = $(this).attr("href");

     if (link && link.startsWith("/")) {
          e.preventDefault();

          $("#page-container").fadeOut(200, function () {
               window.location = link;
          });
     }
});