// Show/hide the boolean field `is_pr_manager`.
// The field has to be extended in admin with CSS class `depended_on_team`.
//
// The logic:
//  - show the field if selected team type is `art`
//  - set "checked" to `false` and hide the field if other partner type is selected

jQuery(document).ready(function ($) {
    let teamTypeSelectField = $("#id_team");
    let divDependedOnTeamType = $(".depended_on_team_type");
    let idIsPrManager = $("#id_is_pr_manager");
    let divHideDatePrManager = $('#festivalteammember_form > div > fieldset.module.aligned.depended_on_team_type > div.form-row.field-data_manager');

    function toggleCheckUndefined(someType, someFunction) {
        if (typeof someType === "undefined") {
            return false;
        } else {
            someFunction(teamTypeSelectField.val());
        }
    }

    function toggleDivDependedOnIsPrManager(inputType) {
        if (inputType === true) {
            divHideDatePrManager.slideDown();
        } else {
        divHideDatePrManager.slideUp();
        }
    }

    function toggleDivDependedOnTeamType(teamType) {
        if (teamType === "art") {
            divDependedOnTeamType.slideDown();
        } else {
        divDependedOnTeamType.slideUp();
        }
    }

    // show/hide on load based on existing value of teamTypeSelectField
    toggleCheckUndefined(teamTypeSelectField.val(), toggleDivDependedOnTeamType)

    // show/hide on load based on existing value of idIsPrManager
    toggleDivDependedOnIsPrManager(idIsPrManager.is(":checked"));
    // show/hide on change
    teamTypeSelectField.change(function () {
        toggleDivDependedOnTeamType($(this).val());
    });
    // show/hide on change
    idIsPrManager.change(function() {
        toggleDivDependedOnIsPrManager(idIsPrManager.is(":checked"));
    });
});
