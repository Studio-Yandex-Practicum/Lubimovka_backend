// Show/hide the boolean field `is_pr_manager`.
// The field has to be extended in admin with CSS class `depended_on_team`.
//
// The logic:
//  - show the field if selected team type is `art`
//  - set "checked" to `false` and hide the field if other partner type is selected

jQuery(document).ready(function ($) {
    let teamTypeSelectField = $("#id_team");
    let isPrManagerField = $("#id_is_pr_manager");
    let divDependedOnTeamType = $(".depended_on_team_type");

    function toggleDivDependedOnTeamType(teamType, isFirstLoad) {
        if (teamType === "art") {
            divDependedOnTeamType.slideDown();
        } else {
            if (isFirstLoad) {
                divDependedOnTeamType.hide();
            } else {
                isPrManagerField.prop("checked", false);
                divDependedOnTeamType.slideUp();
            }
        }
    }

    // show/hide on load based on existing value of teamTypeSelectField
    toggleDivDependedOnTeamType(teamTypeSelectField.val(), true);

    // show/hide on change
    teamTypeSelectField.change(function () {
        toggleDivDependedOnTeamType($(this).val(), false);
    });
});
