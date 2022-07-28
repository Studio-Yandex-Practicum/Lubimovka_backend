jQuery(document).ready(function ($) {
    // source code - required for next step changes (see below)
        $.fn.djangoAdminSelect2 = function(options) {
            var settings = $.extend({}, options);
            $.each(this, function(i, element) {
                var $element = $(element);
                init($element, settings);
            });
            return this;
        };

    // added play_type to request info - required to limit search_result according to play type
    var init = function($element, options) {
        let inlinePlayType = NaN
        if ($element.closest('#author_plays-group').length) {
            inlinePlayType = 'main';
        } else {
            if ($element.closest('#author_plays-2-group').length) {
                inlinePlayType = 'other';
            }
        };
        var settings = $.extend({
            ajax: {
                data: function(params) {
                    return {
                        term: params.term,
                        page: params.page,
                        app_label: $element.data('app-label'),
                        model_name: $element.data('model-name'),
                        field_name: $element.data('field-name'),
                        play_type: inlinePlayType
                    };
                }
            }
        }, options);
        $element.select2(settings);
    };
    jQuery(function($) {
        $('#id_person').on('select2:select', function() {
            var fullName = $('#id_person').select2('data')[0].text;
            $('#id_slug').val(URLify(fullName));
        });
    });
});
