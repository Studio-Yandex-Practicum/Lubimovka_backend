$(document).ready(function(jQuery) {
    jQuery(function($) {
        let linkField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-link');
        let cityField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-city');
        let yearField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-year');
        let urlDownloadField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-url_download');
        let urlReadingField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-url_reading');
        let festivalField = $('#play_form > div > fieldset.module.aligned > div.form-row.field-festival');
        let publishedCheckBox = $('#play_form > div > fieldset.module.aligned > div.form-row.field-published');

        var mainFieldsArray = [cityField, yearField, urlDownloadField, urlReadingField, festivalField, publishedCheckBox]

        var duration = 1

        linkField.hide(duration);

        function toggleLink(slug) {
            if (slug == "other_plays") {
                mainFieldsArray.forEach(function(item) {
                    item.slideUp(duration);
                });
                linkField.slideDown(duration);
            } else {
                mainFieldsArray.forEach(function(item) {
                    item.slideDown(duration);
                });
                linkField.slideUp(duration);

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
    });
});
