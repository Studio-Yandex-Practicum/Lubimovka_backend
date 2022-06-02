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

    // added event_type to request info - required to limit search_result according to event type
    var init = function($element, options) {
        var inlineName = $element.parent().parent().parent().parent().parent().parent().parent().parent().attr('id');
        if (inlineName == "author_plays-group") {
            var inlinePlayType = "main"
        };
        if (inlineName == "author_plays-2-group") {
            var inlinePlayType = "other"
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
});
