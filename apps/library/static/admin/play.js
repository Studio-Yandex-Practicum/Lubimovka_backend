$(document).ready(function(jQuery) {
    jQuery(function($) {
        let type = $('select#id_play_type');
        let linkField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-link');
        let cityField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-city');
        let yearField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-year');
        let urlDownloadField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-url_download');
        let urlReadingField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-url_reading');
        let programField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-program');
        let festivalField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-festival');
        let publishedCheckBox = $('#play_form > div > fieldset.module.aligned > div.form-row.field-published');

        var mainFieldsArray = [cityField, yearField, urlDownloadField, urlReadingField, programField, festivalField, publishedCheckBox]

        var duration = 1

        linkField.hide(duration);

        function toggleLink(inputType) {
            if (inputType == "MAIN") {
                mainFieldsArray.forEach(function(item) {
                    item.slideDown(duration);
                });
                linkField.slideUp(duration);
            } else {
                mainFieldsArray.forEach(function(item) {
                    item.slideUp(duration);
                });
            linkField.slideDown(duration);
            }
        }

        toggleLink(type.val());

        type.change(function() {
            toggleLink(type.val());
        });
    });
});
