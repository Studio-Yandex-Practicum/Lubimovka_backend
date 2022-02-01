// Show/hide the field `in_footer_partner`.
// The field has to be extended in admin with CSS class `depended_on_partner_type`.
//
// The logic:
//  - show the field if selected partner type is `general`
//  - set "checked" to `false` and hide the field if other partner type is selected

jQuery(document).ready(function ($) {
    let partnerTypeSelectField = $('#id_type');
    let inFooterPartnerField = $("#id_in_footer_partner");
    let divDependedOnPartnerType = $(".depended_on_partner_type");

    function toggleDivDependedOnPartnerType(partnerType, isFirstLoad) {
        if (partnerType === 'general') {
            divDependedOnPartnerType.slideDown();
        } else {
            if (isFirstLoad) {
                divDependedOnPartnerType.hide();
            } else {
                inFooterPartnerField.prop("checked", false);
                divDependedOnPartnerType.slideUp();
            }
        }
    }

    // show/hide on load based on existing value of partnerTypeSelectField
    toggleDivDependedOnPartnerType(partnerTypeSelectField.val(), true);

    // show/hide on change
    partnerTypeSelectField.change(function () {
        toggleDivDependedOnPartnerType($(this).val(), false);
    });
});
