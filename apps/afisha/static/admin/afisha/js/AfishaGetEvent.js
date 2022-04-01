// Get CSRF Token for the POST request.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
            url: "/api/v1/afisha/get-common-events-admin/",
            type: "POST",
            data: { type: EventType, },
            success: function (result) {
                cols = document.getElementById('id_common_event');
                cols.options.length = 0;
                for (var event in result) {
                    cols.options.add(new Option(event, result[event]));
                }
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            error: function (e) {
                console.error(JSON.stringify(e));
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
