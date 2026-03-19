$(document).ready(function () {
     // --- Existing Live Search Code ---
     const $searchInput = $('#ajaxSearchInput');
     const $resultsContainer = $('#itemGrid');

     if ($searchInput.length) {
          $searchInput.on('keyup', function () {
               let query = $(this).val();
               $resultsContainer.css('opacity', '0.5');
               $.ajax({
                    url: '/search_items/',
                    data: { 'q': query },
                    dataType: 'html',
                    success: function (data) {
                         $resultsContainer.html(data);
                         $resultsContainer.animate({ opacity: 1 }, 200);
                         applyStaggeredAnimations();
                    }
               });
          });
     }

     // --- NEW: Smooth Category Filtering ---
     $(document).on('click', '.category-link', function (e) {
          e.preventDefault();
          let url = $(this).attr('href');

          // Visually update the active category pill immediately
          $('.category-link').removeClass('btn-gradient text-white').addClass('text-dark');
          $(this).removeClass('text-dark').addClass('btn-gradient text-white');

          // Fade out current grid
          $resultsContainer.css('transition', 'opacity 0.2s ease');
          $resultsContainer.css('opacity', '0.2');

          $.ajax({
               url: url,
               success: function (response) {
                    // Extract only the #itemGrid content from the returned HTML
                    let newContent = $(response).find('#itemGrid').html();

                    // Swap content and fade back in
                    $resultsContainer.html(newContent);
                    $resultsContainer.css('opacity', '1');

                    // Re-trigger the enter animations for new items
                    applyStaggeredAnimations();

                    // Update the browser's URL bar without reloading
                    window.history.pushState({ path: url }, '', url);
               },
               error: function () {
                    $resultsContainer.css('opacity', '1'); // Revert on error
               }
          });
     });

     // Helper function to re-apply animations
     function applyStaggeredAnimations() {
          $('.item-card').each(function (i) {
               $(this).css('animation-delay', (i * 0.05) + 's');
               $(this).addClass('page-enter');
          });
     }

     applyStaggeredAnimations(); // Run on initial load
});