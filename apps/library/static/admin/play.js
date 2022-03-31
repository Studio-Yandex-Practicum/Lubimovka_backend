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
        // slide up and down fields when select program changed by user
        $('select#id_program').on('change', function() {
            toggleLink($('#id_program').val());
        });
        // slide up and down fields when program is already selected (when page was reload, e.g. validation errors)
        $('select#id_program').each(function() {
            toggleLink($('#id_program').val());
        });
    });
});
