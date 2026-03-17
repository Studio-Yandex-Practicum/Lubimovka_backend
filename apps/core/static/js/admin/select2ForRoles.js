jQuery(window).on("load", function () {
    $selectRoleBoxes = $("[id$=roles]");
    $selectRoleBoxes.each(function() {$(this).select2();})
})
