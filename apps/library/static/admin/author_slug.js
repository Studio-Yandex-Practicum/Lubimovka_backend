$(document).ready(function(jQuery) {
    jQuery(function($) {
        $('select#id_person').on('change', function() {
            $.ajax({
                data: $(this).serialize(),
                url: "ajax_author_slug/",
                success: function (response) {
                    $('#id_slug').val(response.slug);
                },
            });
        });
    });
});
