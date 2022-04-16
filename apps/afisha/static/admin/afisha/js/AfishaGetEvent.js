jQuery(document).ready(function ($) {
    let $eventTypeSelectField = $('#id_type');
    let $commonEventField = $("#id_common_event");
    let $divDependedOnCommonEvent = $(".depended_on_common_event");

    function toggleDivDependedOnPartnerType(EventType, isFirstLoad) {
        if (EventType != "") {
            $divDependedOnCommonEvent.slideDown();
        } else {
            if (isFirstLoad) {
                $divDependedOnCommonEvent.hide();
            } else {
                $commonEventField.prop("checked", true);
                $divDependedOnCommonEvent.slideUp();
            }
        };
        $.ajax({
            url: "get-common-events-admin/",
            data: { type: EventType, },
            success: function (result) {
                cols = $('#id_common_event')[0];
                cols.options.length = 0;
                cols.options.add(new Option("", ""));
                for (var event in result) {
                    cols.options.add(new Option(event, result[event]));
                }
            },
            error: function (e) {
                console.log(e);
                alert("Не удалось обработать запрос. Обновите страницу и попробуйте еще раз. Если это не поможет, обратитесь к разработчикам.");
            },
        });
    }

    // show/hide on load based on existing value of partnerTypeSelectField
    toggleDivDependedOnPartnerType($eventTypeSelectField.val(), true);

    // show/hide on change
    $eventTypeSelectField.change(function () {
        toggleDivDependedOnPartnerType($(this).val(), false);
    });
});
