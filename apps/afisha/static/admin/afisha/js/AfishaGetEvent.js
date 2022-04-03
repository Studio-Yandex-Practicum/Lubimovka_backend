jQuery(document).ready(function ($) {
    let EventTypeSelectField = $('#id_type');
    let CommonEventField = $("#id_common_event");
    let divDependedOnCommonEvent = $(".depended_on_common_event");

    function toggleDivDependedOnPartnerType(EventType, isFirstLoad) {
        if (EventType != "") {
            divDependedOnCommonEvent.slideDown();
        } else {
            if (isFirstLoad) {
                divDependedOnCommonEvent.hide();
            } else {
                CommonEventField.prop("checked", false);
                divDependedOnCommonEvent.slideUp();
            }
        };
        $.ajax({
            url: "get-common-events-admin/",
            data: { type: EventType, },
            success: function (result) {
                cols = document.getElementById('id_common_event');
                cols.options.length = 0;
                for (var event in result) {
                    cols.options.add(new Option(event, result[event]));
                }
            },
            error: function (e) {
                console.log(e);
                alert("Не удалось обработать запрос 😞");
            },
        });
    }

    // show/hide on load based on existing value of partnerTypeSelectField
    toggleDivDependedOnPartnerType(EventTypeSelectField.val(), true);

    // show/hide on change
    EventTypeSelectField.change(function () {
        toggleDivDependedOnPartnerType($(this).val(), false);
    });
});
