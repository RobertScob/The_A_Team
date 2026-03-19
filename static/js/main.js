$(document).ready(function () {
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

     $(document).on('click', '.category-link', function (e) {
          e.preventDefault();
          let url = $(this).attr('href');

          $('.category-link').removeClass('btn-gradient text-white').addClass('text-dark');
          $(this).removeClass('text-dark').addClass('btn-gradient text-white');


          $resultsContainer.css('transition', 'opacity 0.2s ease');
          $resultsContainer.css('opacity', '0.2');

          $.ajax({
               url: url,
               success: function (response) {

                    let newContent = $(response).find('#itemGrid').html();


                    $resultsContainer.html(newContent);
                    $resultsContainer.css('opacity', '1');


                    applyStaggeredAnimations();


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