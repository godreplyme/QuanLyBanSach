$(document).ready(function() {
    const mainImage = $('#mainImage');
    const originalSrc = mainImage.attr('src');

    $('.thumbnail').hover(
        function() {
            // Mouse enters the thumbnail
            const newSrc = $(this).attr('src');
            mainImage.attr('src', newSrc);
        },
        function() {
            // Mouse leaves the thumbnail
            mainImage.attr('src', originalSrc);
        }
    );
});

