$(document).ready(function () {
     // AJAX Live Search function
     const $searchInput = $('#ajaxSearchInput');
     const $resultsContainer = $('#itemGrid');

     if ($searchInput.length) {
          $searchInput.on('keyup', function () {
               let query = $(this).val();

               // Add a simple loading state class
               $resultsContainer.css('opacity', '0.5');

               $.ajax({
                    url: '/search_items/', // Make sure this matches your urls.py path
                    data: {
                         'q': query
                    },
                    dataType: 'html',
                    success: function (data) {
                         // Inject the returned HTML component
                         $resultsContainer.html(data);
                         // Fade back in smoothly
                         $resultsContainer.animate({ opacity: 1 }, 200);
                    },
                    error: function () {
                         console.error("Failed to fetch search results.");
                         $resultsContainer.css('opacity', '1');
                    }
               });
          });
     }

     // Apply animation stagger to item cards on load
     $('.item-card').each(function (i) {
          $(this).css('animation-delay', (i * 0.05) + 's');
          $(this).addClass('page-enter');
     });
});