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
        }
    }

    // show/hide on load based on existing value of partnerTypeSelectField
    toggleDivDependedOnPartnerType(EventTypeSelectField.val(), true);

    // show/hide on change
    EventTypeSelectField.change(function () {
        toggleDivDependedOnPartnerType($(this).val(), false);
    });
});
