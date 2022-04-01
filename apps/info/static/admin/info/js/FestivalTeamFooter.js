// Show/hide the field `data_director`.
// The field has to be extended in admin with CSS class `form-row field-data_director`.
//
// The logic:
//  - show the field if boolean field `is_pr_director` is `true`

jQuery(document).ready(function ($) {
    let idIsPrDirector = $("#id_is_pr_director");
    let divHideDatePrDirector = $(".form-row .field-data_director")

    // exit from function if there isn't selector
    if (!idIsPrDirector.length) {
        return false
    }
    // hide the field `data_director`.
    divHideDatePrDirector.hide();

    function toggleDivDependedOnIsPrDirector(inputType) {
         if (inputType) {
            divHideDatePrDirector.slideDown();
         } else {
            divHideDatePrDirector.slideUp();
         }
     }

    // show/hide on load based on existing value of idIsPrDirector
    toggleDivDependedOnIsPrDirector(idIsPrDirector.is(":checked"));

    // show/hide on change
    idIsPrDirector.change(function() {
        toggleDivDependedOnIsPrDirector(idIsPrDirector.is(":checked"));
    });
});
