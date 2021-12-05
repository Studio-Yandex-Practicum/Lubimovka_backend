jQuery(document).ready(function ($) {
    (function ($) {
        $(function () {
            var selectField = $('#id_type'),
                verified = $('.included');

            function toggleVerified(value) {
                if (value === 'general') {
                    verified.show();
                } else {
                    verified.hide();
                }
            }

            // show/hide on load based on existing value of selectField
            toggleVerified(selectField.val());

            // show/hide on change
            selectField.change(function () {
                toggleVerified($(this).val());
            });
        });
    })(django.jQuery);
});
