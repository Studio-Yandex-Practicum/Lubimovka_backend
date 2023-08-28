const select2_settings = {
    closeOnSelect : true,
    placeholder: "...", // required for allowClear function to work
    allowClear: true,
    dropdownAutoWidth: true,
    width: ""
}

django.jQuery(document).ready(function(){
    django.jQuery("tr:not(.empty-form) td.field-roles select").select2(select2_settings);
})
django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
    // Row added
    if (formsetName === "extended_persons"){
        $row.children("td.field-roles").children("select").select2(select2_settings)
    }
});
