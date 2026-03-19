$(document).ready(function () {

     $("#searchInput").on("keyup", function () {

          let query = $(this).val();

          $.ajax({
               url: "/search/",
               data: { q: query },

               success: function (data) {
                    $("#items-container").html(data);
               }
          });

     });

});