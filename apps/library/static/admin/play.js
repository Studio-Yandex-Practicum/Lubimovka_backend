$(document).ready(function(jQuery) {
    jQuery(function($) {
        let cityField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-city');
        let yearField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-year');
        let urlReadingField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-url_reading');
        let festivalField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-festival');
        let programField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-program');

        var mainFieldsArray = [cityField, yearField, urlReadingField, festivalField, programField];

        var duration = 1;

        function toggleLink(type) {
            if (type) {
                mainFieldsArray.forEach(function(item) {
                    item.slideDown(duration);
                });
            } else {
                mainFieldsArray.forEach(function(item) {
                    item.slideUp(duration);
                });
            }
        };

        toggleLink($('#id_type').is(':checked'));
        $('#id_type').change(function() {
            toggleLink($('#id_type').is(':checked'));
        });
    });
});
