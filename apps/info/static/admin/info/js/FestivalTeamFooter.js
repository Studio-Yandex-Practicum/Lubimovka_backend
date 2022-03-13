// Show/hide the field `data_manager`.
// The field has to be extended in admin with CSS class `form-row field-data_manager`.
//
// The logic:
//  - show the field if boolean field `is_pr_manager` is `true`

jQuery(document).ready(function ($) {
    let idIsPrManager = $("#id_is_pr_manager");
    let divHideDatePrManager = $("#artteammember_form > div > fieldset:nth-child(2) > div.form-row.field-data_manager");

    // exit from function if there isn't selector
    if (!idIsPrManager.length) {
        return false
    }
    // hide the field `data_manager`.
    divHideDatePrManager.hide();

    function toggleDivDependedOnIsPrManager(inputType) {
         if (inputType) {
             divHideDatePrManager.slideDown();
         } else {
         divHideDatePrManager.slideUp();
         }
     }

    // show/hide on load based on existing value of idIsPrManager
    toggleDivDependedOnIsPrManager(idIsPrManager.is(":checked"));

    // show/hide on change
    idIsPrManager.change(function() {
        toggleDivDependedOnIsPrManager(idIsPrManager.is(":checked"));
    });
});
