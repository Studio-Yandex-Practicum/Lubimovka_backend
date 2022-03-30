$(document).ready(function(jQuery) {
    jQuery(function($) {
        let cityField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-city');
        let yearField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-year');
        let urlReadingField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-url_reading');
        let festivalField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-festival');

        var mainFieldsArray = [cityField, yearField, urlReadingField, festivalField]

        var duration = 1;

        function toggleLink(slug) {
            if (slug == "other_plays") {
                mainFieldsArray.forEach(function(item) {
                    item.slideUp(duration);
                });
            } else {
                mainFieldsArray.forEach(function(item) {
                    item.slideDown(duration);
                });
            }
        };

        $('select#id_program').on('change', function() {
            $.ajax({
                data: $(this).serialize(),
                url: "ajax_play_program/",
                success: function (response) {
                    let slug = response.slug
                    toggleLink(slug);
                },
            });
        });
        $('select#id_program').each(function() {
            $.ajax({
                data: $(this).serialize(),
                url: "ajax_play_program/",
                success: function (response) {
                    let slug = response.slug
                    toggleLink(slug);
                },
            });
        });
    });
});
