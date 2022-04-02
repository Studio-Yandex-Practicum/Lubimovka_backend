// Show/hide the field `pr_director_name`.
// The field has to be extended in admin with CSS class `form-row field-pr_director_name`.
//
// The logic:
//  - show the field if boolean field `is_pr_director` is `true`

jQuery(document).ready(function ($) {
    let idIsPrDirector = $("#id_is_pr_director");
    let divHideDatePrDirector = $(".form-row .field-pr_director_name")

    // exit from function if there isn't selector
    if (!idIsPrDirector.length) {
        return false
    }
    // hide the field `pr_director_name`.
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
