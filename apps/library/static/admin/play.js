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

        linkField.hide(1);

        function toggleLink(inputType) {
            if (inputType == "MAIN") {
                cityField.slideDown(1);
                yearField.slideDown(1);
                urlDownloadField.slideDown(1);
                urlReadingField.slideDown(1);
                programField.slideDown(1);
                festivalField.slideDown(1);
                publishedCheckBox.slideDown(1);
                linkField.slideUp(1);
            } else {
            cityField.slideUp(1);
            yearField.slideUp(1);
            urlDownloadField.slideUp(1);
            urlReadingField.slideUp(1);
            programField.slideUp(1);
            festivalField.slideUp(1);
            publishedCheckBox.slideUp(1);
            linkField.slideDown(1);
            }
        }

        toggleLink(type.val());

        type.change(function() {
            toggleLink(type.val());
        });
    });
});
