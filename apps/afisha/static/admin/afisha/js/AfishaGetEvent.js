jQuery(document).ready(function ($) {
    let $eventTypeSelectField = $('#id_type');
    let $divDependedOnCommonEvent = $(".depended_on_common_event");

    function toggleDivDependedOnPartnerType(eventType, isFirstLoad) {
        if (eventType === undefined) {
            return;
        }
        if (eventType != "") {
            $divDependedOnCommonEvent.slideDown();
        } else {
            if (isFirstLoad) {
                $divDependedOnCommonEvent.hide();
            } else {
                $divDependedOnCommonEvent.slideUp();
            }
        };
        $.ajax({
            url: "get-common-events-admin/",
            data: { type: eventType, },
            success: function (result) {
                cols = $('#id_common_event')[0];
                var selected = cols.options.item(cols.options.selectedIndex)
                cols.options.length = 0;
                if (isFirstLoad === false) {
                    cols.options.add(new Option("", ""));
                } else {
                    cols.options.add(selected);
                }
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
